import asyncio
import time
import re
import sys
from claude_agent_sdk import (
  query,
  create_sdk_mcp_server,
  ClaudeAgentOptions,
  TextBlock,
  ToolUseBlock,
  AssistantMessage,
  ResultMessage,
  UserMessage,
  ToolResultBlock
)

from agents import (
  web_search_agent,
  # doc_analysis_agent
)

import web_researcher.tools as web_researcher_tools
# import doc_analyst.tools as doc_analyst_tools

PROMPT = "Research the impact of AI on creative industries."
SYSTEM_PROMPT = '''
You are an automated Research Agent specfialized in coordinating agents that will perform searches, analysis and present results in JSON format.

Your main goal is to research delegating specific tasks to specialized search and analysis subagents. For this specific research exercise you'll have
a delimited universe of sources, all those sources can only be accessed by using the declared tools.

Don't use any other information, don't complete with your own information and for this research exercise you are not allowed to perform any search
from the outside..
'''

server = create_sdk_mcp_server(
  name="research_analysis",
  version="1.0.0",
  tools=[
    web_researcher_tools.search_web
  ]
)

def getTime(text):
  if not isinstance(text, str):
    text = str(text)
  match = re.search(r"duration_ms:\s*(\d+)", text)
  if match:
    return int(match.group(1))
  return 0


async def main():
  total_subagents_time_ms = 0
  
  async for message in query(
    prompt=PROMPT,
    options=ClaudeAgentOptions(
      model="claude-opus-5",
      system_prompt=SYSTEM_PROMPT,
      permission_mode="acceptEdits",
      allowed_tools=["Agent", "mcp__research_analysis__search_web"],
      agents={"web_search": web_search_agent },
      mcp_servers={"research_analysis": server}
    ),
  ):
    if isinstance(message, AssistantMessage):
      for block in message.content:
        if isinstance(block, TextBlock):
          print(block.text)        
        elif isinstance(block, ToolUseBlock):
          print(f"Tool: {block.name}")
      
      print("-----------------------------------")
          
    if isinstance(message, UserMessage):
      for block in message.content:
        if isinstance(block, TextBlock):
          print(block.text)
        elif isinstance(block, ToolResultBlock):
          total_subagents_time_ms += getTime(block.content)
          print(f"Tool Result: {block.content}, Is error: {block.is_error}")
    
    elif isinstance(message, ResultMessage):
      print(f"Done: {message.subtype}")
      
      
  return total_subagents_time_ms

if __name__ == "__main__":
    start = time.perf_counter()
    
    try:
        sum_subagents_ms = asyncio.run(main())
    finally:
      end = time.perf_counter()      
      total_execution_time = end - start
      print(f"Agent loop took {total_execution_time: .4f} seconds")
      
      sum_subagents_sec = sum_subagents_ms / 1000
      print(f"Subagents execution sumatory {sum_subagents_sec: .4f} seconds")
      
      sys.stdout.flush()