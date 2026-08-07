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
  query = args.get("query")
  
  if not query:
    return {
      "content": [{"type": "text", "text": "Query cannot be None or empty"}],
      "is_error": True
    }
  
  stop_words = {"in", "of", "on", "a", "the", "for", "to", "and"}
  words = [
      w.lower()
      for w in query.split()
      if w.lower() not in stop_words and len(w) > 1
  ]
  
  if not words:
    return {"content": [{"type": "text", "text": json.dumps([])}]}
  
  findings = []
  
  for item in raw_web_database():
      content = item["content"].lower()
      title = item["title"].lower()
      
      if all(w in content or w in title for w in words):
        findings.append(item)

  return {"content": [{"type": "text", "text": json.dumps(findings)}]}