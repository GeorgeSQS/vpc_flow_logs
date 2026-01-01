from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os
import logging
from app.models import CartItem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("frontend_app")

# Backend Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "http://localhost:8001")

app = FastAPI(title="CloudMart Frontend")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

async def fetch_from_backend(endpoint: str):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{BACKEND_HOST}{endpoint}"
            logger.info(f"Frontend: Forwarding GET to {url}")
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching from backend: {e}")
            return None

@app.get("/health")
async def health_check():
    # Frontend health check
    return {"status": "frontend_healthy"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = await fetch_from_backend("/api/products") or []
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    product = await fetch_from_backend(f"/api/products/{product_id}")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("product.html", {"request": request, "product": product})

@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})

# Proxy Routes for Client-Side JS
@app.get("/api/products/{product_id}")
async def proxy_get_product(product_id: str):
    data = await fetch_from_backend(f"/api/products/{product_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    return data

@app.post("/api/cart")
async def proxy_add_to_cart(item: CartItem):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{BACKEND_HOST}/api/cart"
            logger.info(f"Frontend: Forwarding POST to {url}")
            response = await client.post(url, json=item.model_dump(), timeout=5.0)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/checkout")
async def proxy_checkout(items: list[CartItem]):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{BACKEND_HOST}/api/checkout"
            # Serialize list of models
            json_data = [item.model_dump() for item in items]
            logger.info(f"Frontend: Forwarding POST to {url}")
            response = await client.post(url, json=json_data, timeout=5.0)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
