from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image_url: str

class CartItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    order_id: str
    items: List[CartItem]
    total_amount: float
    status: str
