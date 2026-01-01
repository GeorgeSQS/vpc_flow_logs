from app.models import Product

# Mock Database
PRODUCTS = [
    Product(
        id="1",
        name="Quantum Widget",
        description="A high-performance widget for quantum computing tests.",
        price=199.99,
        image_url="https://via.placeholder.com/300?text=Quantum+Widget"
    ),
    Product(
        id="2",
        name="Hyper-Threaded Bobbin",
        description="Thread your code with hyper-speed precision.",
        price=49.50,
        image_url="https://via.placeholder.com/300?text=Hyper+Bobbin"
    ),
    Product(
        id="3",
        name="Nano-Fiber Cable",
        description="Lossless data transmission over short distances.",
        price=12.99,
        image_url="https://via.placeholder.com/300?text=Nano+Cable"
    ),
    Product(
        id="4",
        name="Flux Capacitor",
        description="Time travel not included.",
        price=12000.00,
        image_url="https://via.placeholder.com/300?text=Flux+Capacitor"
    ),
    Product(
        id="5",
        name="Infinite Loop Donut",
        description="Tastes like forever.",
        price=5.00,
        image_url="https://via.placeholder.com/300?text=Infinite+Donut"
    ),
    Product(
        id="6",
        name="Null Pointer Exception",
        description="The most classic gift for a developer.",
        price=0.00,
        image_url="https://via.placeholder.com/300?text=Null+Pointer"
    ),
]

def get_product(product_id: str):
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    return None
