from typing import Any
from claude_agent_sdk import tool
import json

customers = [
  { "id": "1", "name": "john", "lastname": "doe", "age": 20 },
  { "id": "2", "name": "frankie", "lastname": "edgar", "age": 45 },
  { "id": "3", "name": "alexa", "lastname": "grasso", "age": 30 },
  { "id": "4", "name": "brandon", "lastname": "moreno", "age": 34 },
  { "id": "5", "name": "miesha", "lastname": "tate", "age": 47 },
]

orders = [
  { "id": "101", "customer_id": "1", "product": "Laptop", "total": 1200.00, "status": "paid" },
  { "id": "102", "customer_id": "3", "product": "Smartphone", "total": 800.00, "status": "authorized" },
  { "id": "103", "customer_id": "2", "product": "Guantes de MMA", "total": 75.50, "status": "refunded" },
  { "id": "104", "customer_id": "4", "product": "Protein Powder", "total": 50.00, "status": "canceled" },
  { "id": "105", "customer_id": "1", "product": "Mouse Gamer", "total": 25.00, "status": "paid" },
  { "id": "106", "customer_id": "2", "product": "Xbox control", "total": 250, "status": "paid" },
  { "id": "107", "customer_id": "3", "product": "Samsung Galaxy", "total": 699, "status": "paid" },
]

@tool(
  "get_customer",
  "Retrieves the details of a customer using their unique customer ID.",
  { "id": str }
)
async def get_customer(args: dict[str, Any]) -> dict[str, Any]:
  customer_id = args["id"]

  customer = next((c for c in customers if c["id"] == customer_id), None)

  if customer is None:
    return {
      "content": [
        {"type": "text", "text": f"Customer with the id {customer_id} not found"}
      ],
      "is_error": True,
    }

  return {"content": [{"type": "text", "text": json.dumps(customer)}]}


@tool(
  "lookup_order",
  "Looks up the details of a specific order using its order ID, returning information like the product, total, and status.",
  { "order_id": str }
)
async def lookup_order(args: dict[str, Any]) -> dict[str, Any]:
  order_id = args["order_id"]
    
  # Buscamos la orden en la nueva lista 'orders'
  order = next((o for o in orders if o["id"] == order_id), None)
  
  if order is None:
    return {
      "content": [
        {"type": "text", "text": f"Order with the id {order_id} not found"}
      ],
      "is_error": True,
    }
    
  return {"content": [{"type": "text", "text": json.dumps(order)}]}

@tool(
  "process_refund",
  "Processes a refund for a specific order. The order must currently have a 'paid' status to be refunded successfully.",
  { "order_id": str }
)
async def process_refund(args: dict[str, Any]) -> dict[str, Any]:
  order_id = args["order_id"]
  order = next((o for o in orders if o["id"] == order_id), None)
  
  if order is None:
    return {
      "content": [
        {"type": "text", "text": f"Order with the id {order_id} not found"}
      ],
      "is_error": True,
    }
  
  if order["status"] == "refunded":
    return {
      "content": [
        {"type": "text", "text": f"Order with the id {order_id} is already refunded"}
      ],
      "is_error": True,
    }
  
  if order["status"] != "paid":
    return {
      "content": [
        {"type": "text", "text": f"Order {order_id} status needs to be paid to be refunded"}
      ],
      "is_error": True,
    }
  
  order["status"] = "refunded"
  return {"content": [{"type": "text", "text": json.dumps(order)}]}


@tool(
  "escalate_to_human",
  "Escalates an order issue to a human support agent. Use this when a refund fails, the user is angry, or an action cannot be completed automatically.",
  { "order_id": str, "reason": str }
)
async def escalate_to_human(args: dict[str, Any]) -> dict[str, Any]:
  order_id = args["order_id"]
  reason = args["reason"]
  order = next((o for o in orders if o["id"] == order_id), None)
  
  if order is None:
    return {
      "content": [
        {"type": "text", "text": f"Order with the id {order_id} not found"}
      ],
      "is_error": True,
    }
  
  order["escalated"] = True
  
  copy = order.copy()
  copy["reason"] = reason
  
  return {"content": [{"type": "text", "text": json.dumps(copy)}]}
