import os
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message
import json

import tools

load_dotenv()

client = Anthropic()
MODEL = "claude-sonnet-4-6"

my_tools = [
  tools.get_customer_schema,
  tools.lookup_order_schema,
  tools.process_refund_schema,
  tools.escalate_to_human_schema
]

# Anthropic Helper Functions
def add_user_messages(messages, message):
  user_message = { 
    "role": "user",
    "content": message.content if isinstance(message, Message) else message,
  }
  messages.append(user_message)
  
def add_assistant_message(messages, message):
  assistant_message = { 
    "role": "assistant",
    "content": message.content if isinstance(message, Message) else message,
  }
  messages.append(assistant_message)
  
def chat(messages, max_tokens=1000, system=None, temperature=1.0, tools_def=None):
  params = {
    "model": MODEL,
    "max_tokens": max_tokens,
    "messages": messages,
    "temperature": temperature
  }
  
  if system:
    params["system"] = system
    
  if tools_def:
    params["tools"] = tools_def
    
  message = client.messages.create(**params)
  return message
    
def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])

# Run Tool Helper Functions
def run_tool(tool_name, tool_input):
  if tool_name == "get_customer":
    return tools.get_customer(**tool_input)
  if tool_name == "lookup_order":
    return tools.lookup_order(**tool_input)
  if tool_name == "process_refund":
    return tools.process_refund(**tool_input)
  if tool_name == "escalate_to_human":
      return tools.escalate_to_human(**tool_input)
  else:
    raise ValueError(f"Unknown tool: {tool_name}")
  

def get_tool_result_block(tool_request_id, tool_output, is_error):
  return {
    "type": "tool_result",
    "tool_use_id": tool_request_id,
    "content": f"Error: {tool_output}" if is_error == True else json.dumps(tool_output),
    "is_error": is_error
  }
  
def run_tools(message):
  tool_requests = [block for block in message.content if block.type == "tool_use"]
  tool_result_blocks = []
  
  print(tool_requests)
  
  for tool_request in tool_requests:
    print(f"tool_request: {tool_request.name} with inputs: {tool_request.input}")
    try:
      tool_output = run_tool(tool_request.name, tool_request.input)
      tool_response = get_tool_result_block(tool_request.id, tool_output, False)
    except Exception as e:
      # TODO inject structured error in step 3 of the project
      tool_response = get_tool_result_block(tool_request.id, e, True)
      
    tool_result_blocks.append(tool_response)
    
  return tool_result_blocks


def run_agent_loop(messages):
  while True:
    response = chat(
      messages,
      max_tokens=1000,
      tools_def = my_tools
    )
    
    # Respond directly to the previous messages existed into messages list
    add_assistant_message(messages, response)
    
    if response.stop_reason == "tool_use":
      tool_results = run_tools(response)
      add_user_messages(messages, tool_results)
      
    elif response.stop_reason == "end_turn":
      # Extract text from the message response and print it
      print(text_from_message(response))
      break
    
    elif response.stop_reason == "max_tokens":
      print("Max tokens reached!")
      break
    
    else:
      print(f"Not supported stop reason {response.stop_reason}")    
  return messages


messages = []

add_user_messages(
  messages,
  "refund order 103 and tell me the status of order 102"
)

run_agent_loop(messages)
      
