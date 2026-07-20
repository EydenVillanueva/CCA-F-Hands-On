
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
  
  
def lookup_order(order_id):
  if order_id is None:
    raise ValueError("Required parameter order_id cannot be None")
    
  # Buscamos la orden en la nueva lista 'orders'
  order = next((o for o in orders if o["id"] == order_id), None)
  
  if order is None:
    raise ValueError(f"Order with the id {order_id} not found")
    
  return order

def process_refund(order_id):
  order = lookup_order(order_id)
  
  if order["status"] == "refunded":
    raise ValueError(f"Order with the id {order_id} is already refunded")
  
  if order["status"] != "paid":
    raise ValueError(f"Order {order["id"]} status needs to be paid to be refunded")
  
  order["status"] = "refunded"
  return order


def escalate_to_human(order_id, reason):
  order = lookup_order(order_id)
  order["escalated"] = True
  
  copy = order.copy()
  copy["reason"] = reason
  
  return copy
