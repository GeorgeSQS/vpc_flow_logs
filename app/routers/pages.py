from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.db import PRODUCTS, get_product
import logging

# Configure logging
logger = logging.getLogger("vpc_app_frontend")

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    logger.info("Frontend: Serving data for Home Page")
    return templates.TemplateResponse("index.html", {"request": request, "products": PRODUCTS})

@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    logger.info(f"Frontend: Serving product page for {product_id}")
    product = get_product(product_id)
    if not product:
        # In a real app we'd show a 404 template
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("product.html", {"request": request, "product": product})

@router.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    # The cart data will be loaded from client side storage and hydrated via API calls 
    # OR we just show the cart page and let JS do the logic
    logger.info("Frontend: Serving Cart Page")
    return templates.TemplateResponse("cart.html", {"request": request})

@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    logger.info("Frontend: Serving Checkout Page")
    return templates.TemplateResponse("checkout.html", {"request": request})
