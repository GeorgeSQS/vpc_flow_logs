from fastapi import FastAPI, HTTPException, status
from typing import List
from app.models import Product, CartItem, Order
from app.db import PRODUCTS, get_product
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend_api")

app = FastAPI(title="CloudMart Backend", docs_url="/docs", openapi_url="/openapi.json")

@app.get("/health")
async def health_check():
    return {"status": "backend_healthy", "service": "backend"}

@app.get("/api/products", response_model=List[Product])
async def list_products():
    logger.info("Backend: Fetching product list")
    return PRODUCTS

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product_detail(product_id: str):
    logger.info(f"Backend: Fetching product {product_id}")
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/cart")
async def add_to_cart(item: CartItem):
    logger.info(f"Backend: Adding product {item.product_id} to cart (Qty: {item.quantity})")
    product = get_product(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Item added to cart", "item": item}

@app.post("/api/checkout", response_model=Order)
async def checkout(cart_items: List[CartItem]):
    logger.info(f"Backend: Checkout request with {len(cart_items)} items")
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_amount = 0.0
    confirmed_items = []
    
    for item in cart_items:
        product = get_product(item.product_id)
        if product:
            total_amount += product.price * item.quantity
            confirmed_items.append(item)
    
    order = Order(
        order_id=str(uuid.uuid4()),
        items=confirmed_items,
        total_amount=round(total_amount, 2),
        status="confirmed"
    )
    
    logger.info(f"Backend: Order confirmed {order.order_id}")
    return order
