from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import api, pages
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

app = FastAPI(
    title="VPC Flow Log Traffic Generator",
    description="E-commerce simulation to generate VPC Flow Logs",
    version="1.0.0"
)

# Mount Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include Routers
app.include_router(api.router)
app.include_router(pages.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
