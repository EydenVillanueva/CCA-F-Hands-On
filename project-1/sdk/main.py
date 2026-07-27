import asyncio
from claude_agent_sdk import (
  query,
  create_sdk_mcp_server,
  ClaudeAgentOptions,
  AssistantMessage,
  ResultMessage,
  TextBlock,
  ToolUseBlock
)
import tools


#system_prompt
system_prompt = '''
  You're an automated customer support agent that will provide the user with the asked information about
  customers information (id, name, lastname, address, age), order information (id, customer_id, product, total and status )
  and provide refunds and escalation depending on the specific order information.
  
  Said that these are the business rules:
  
  1) When a user ask for refund an order the order needs to be in 'paid' status and the order total needs to be below 700$
  And this is the only case where you can refund an order as an automated agent. (order total < 700$ and status = 'paid')
  
  2) When the user wants to refund an order on 700$ or above, the order status is not longer relevant (it could be 'paid', 'refunded', 'canceled' etc)
  You, as an automated customer support agent will need to escalate this to a human using the escalate_to_human provided tool.
  And the refund will be perform manually after a human inspection of the order.
'''

# Server
server = create_sdk_mcp_server(
  name="crm-tools",
  version="1.0.0",
  tools=[
    tools.get_customer,
    tools.lookup_order,
    tools.process_refund,
    tools.escalate_to_human
  ]
)

async def main():
  async for message in query(
    prompt="refund order 102, 101 return me the information of customer 1, 2 the address of customer 5 and refund me the order 107",
    options=ClaudeAgentOptions(
      model="claude-sonnet-5",
      permission_mode="acceptEdits",
      system_prompt=system_prompt,
      mcp_servers={"crm": server},
      allowed_tools=["Agent", "mcp__crm__get_customer", "mcp__crm__lookup_order", "mcp__crm__process_refund", "mcp__crm__escalate_to_human"]
    ),
  ):
    if isinstance(message, AssistantMessage):
      for block in message.content:
        if isinstance(block, TextBlock):
          print(block.text)
        elif isinstance(block, ToolUseBlock):
          print(f"Tool: {block.name}")
    
    elif isinstance(message, ResultMessage):
      print(f"Done: {message.subtype}")

asyncio.run(main())