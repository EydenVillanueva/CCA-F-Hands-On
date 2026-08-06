from typing import Any
from claude_agent_sdk import tool
import json
from fixtures.web_corpus import raw_web_database


@tool(
  "search_web",
  "Retrieves all the information sources related to a specific query by using a substring matching",
  {"query": str}
)
async def search_web(args: dict[str, Any]) -> dict[str, Any]:
  query = args["query"]
  
  if query is None:
    return {
      "content": [
        {"type": "text", "text": f"Query cannot be None"}
      ],
      "is_error": True
    }
  
  findings = []  
  
  for item in raw_web_database():
    content = item["content"].lower()
    title = item["title"].lower()        
    for word in query.split():
      word = word.lower()
      if word in content or word in title:
        findings.append(item)
    
  return {
    "content": [{
      "type": "text",
      "text": json.dumps(findings)
    }]
  }