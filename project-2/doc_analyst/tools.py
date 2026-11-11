from typing import Any
from claude_agent_sdk import tool
import json
from fixtures.doc_corpus import raw_documents_repository


@tool(
  "doc_analyst",
  "Retrieves all the available documents related to an specific query by using a substring matching",
  {"query": str}
)
async def doc_analyst(args: dict[str,Any]) -> dict[str, Any]:
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
  
  for item in raw_documents_repository():
      content = item["content"].lower()
      title = item["document_name"].lower()
      
      if all(w in content or w in title for w in words):
        findings.append(item)

  return {"content": [{"type": "text", "text": json.dumps(findings)}]}  
