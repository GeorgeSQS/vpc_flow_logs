from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Product, CartItem, Order
from app.db import PRODUCTS, get_product
import uuid
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vpc_app_api")

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
async def health_check():
    """Health check endpoint for load balancer probing."""
    return {"status": "healthy"}

@router.get("/products", response_model=List[Product])
async def list_products():
    """List all available products."""
    logger.info("API: Fetching product list")
    return PRODUCTS

@router.get("/products/{product_id}", response_model=Product)
async def get_product_detail(product_id: str):
    """Get details of a specific product."""
    logger.info(f"API: Fetching product {product_id}")
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/cart")
async def add_to_cart(item: CartItem):
    """
    Simulate adding item to cart. 
    In a real app, this would update a session or database.
    Here strictly to generate traffic.
    """
    logger.info(f"API: Adding product {item.product_id} to cart with quantity {item.quantity}")
    product = get_product(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Item added to cart", "item": item}

@router.post("/checkout", response_model=Order)
async def checkout(cart_items: List[CartItem]):
    """
    Simulate checkout process.
    Calculates total and returns an order confirmation.
    """
    logger.info(f"API: Checkout request with {len(cart_items)} items")
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
    
    logger.info(f"API: Order confirmed {order.order_id} - Total: ${order.total_amount}")
    return order
