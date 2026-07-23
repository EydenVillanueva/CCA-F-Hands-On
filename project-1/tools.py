from anthropic.types import ToolParam

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
]


# Tool Definition
def get_customer(id):
  if id is None:
    raise ValueError(
      "Required parameter id cannot be None"
    )
        
  customer = next((c for c in customers if c["id"] == id), None)
  
  if customer is None:
    raise ValueError(
      f"Customer with the id ${id} not found"
    )
    
  return customer 

get_customer_schema: ToolParam = {
    "name": "get_customer",
    "description": "Retrieves the details of a customer using their unique customer ID.",
    "input_schema": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The unique identifier of the customer (e.g., '1', '2', '3')."
            }
        },
        "required": ["id"]
    }
}

def lookup_order(order_id):
  if order_id is None:
    raise ValueError("Required parameter order_id cannot be None")
    
  # Buscamos la orden en la nueva lista 'orders'
  order = next((o for o in orders if o["id"] == order_id), None)
  
  if order is None:
    raise ValueError(f"Order with the id {order_id} not found")
    
  return order

lookup_order_schema: ToolParam = {
    "name": "lookup_order",
    "description": "Looks up the details of a specific order using its order ID, returning information like the product, total, and status.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The unique identifier of the order (e.g., '101', '102')."
            }
        },
        "required": ["order_id"]
    }
}

def process_refund(order_id):
  order = lookup_order(order_id)
  
  if order["status"] == "refunded":
    raise ValueError(f"Order with the id {order_id} is already refunded")
  
  if order["status"] != "paid":
    raise ValueError(f"Order {order["id"]} status needs to be paid to be refunded")
  
  order["status"] = "refunded"
  return order

process_refund_schema: ToolParam = {
    "name": "process_refund",
    "description": "Processes a refund for a specific order. The order must currently have a 'paid' status to be refunded successfully.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The unique identifier of the order to refund."
            }
        },
        "required": ["order_id"]
    }
}

def escalate_to_human(order_id, reason):
  order = lookup_order(order_id)
  order["escalated"] = True
  
  copy = order.copy()
  copy["reason"] = reason
  
  return copy

escalate_to_human_schema: ToolParam = {
    "name": "escalate_to_human",
    "description": "Escalates an order issue to a human support agent. Use this when a refund fails, the user is angry, or an action cannot be completed automatically.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The unique identifier of the order being escalated."
            },
            "reason": {
                "type": "string",
                "description": "A detailed explanation of why the issue needs human intervention."
            }
        },
        "required": ["order_id", "reason"]
    }
}
