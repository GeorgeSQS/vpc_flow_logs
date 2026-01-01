// Cart Management
function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}

function setCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(productId) {
    let cart = getCart();
    const existing = cart.find(item => item.product_id === productId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ product_id: productId, quantity: 1 });
    }
    setCart(cart);
    
    // GENERATE TRAFFIC: Send to backend
    fetch('/api/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
    }).catch(console.error);

    showToast("Added to cart!");
}

function updateCartCount() {
    const cart = getCart();
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    const el = document.getElementById('cart-count');
    if (el) el.innerText = `(${count})`;
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Cart Page Logic
async function loadCartDisplay() {
    const container = document.getElementById('cart-container');
    if (!container) return; // Not on cart page

    const cart = getCart();
    if (cart.length === 0) {
        container.innerHTML = '<p style="text-align:center; padding: 2rem;">Your cart is empty.</p>';
        document.getElementById('cart-total').innerText = '$0.00';
        return;
    }

    container.innerHTML = '';
    let total = 0;

    // Fetch details for all items (Generates Traffic!)
    // We use Promise.all to fetch parallels or loop for sequential (sequential is fine, generates steady traffic stream)
    for (const item of cart) {
        try {
            const res = await fetch(`/api/products/${item.product_id}`);
            if (!res.ok) continue;
            const product = await res.json();
            
            const itemTotal = product.price * item.quantity;
            total += itemTotal;

            const div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = `
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem;">${product.name}</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">$${product.price} x ${item.quantity}</div>
                </div>
                <div style="font-weight: 700;">$${itemTotal.toFixed(2)}</div>
            `;
            container.appendChild(div);
        } catch (e) {
            console.error(e);
        }
    }

    document.getElementById('cart-total').innerText = '$' + total.toFixed(2);
}

async function checkout() {
    const cart = getCart();
    if (cart.length === 0) {
        showToast("Cart is empty!");
        return;
    }
    
    const btn = document.querySelector('button[onclick="checkout()"]');
    if (btn) {
        btn.innerText = "Processing...";
        btn.disabled = true;
    }

    // GENERATE TRAFFIC
    try {
        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cart)
        });
        
        if (res.ok) {
            const order = await res.json();
            window.location.href = `/checkout?order_id=${order.order_id}`;
        } else {
            showToast("Checkout failed.");
            if (btn) {
                btn.innerText = "Proceed to Checkout";
                btn.disabled = false;
            }
        }
    } catch (e) {
        console.error(e);
        showToast("Error during checkout.");
        if (btn) {
            btn.innerText = "Proceed to Checkout";
            btn.disabled = false;
        }
    }
}

// Init
document.addEventListener('DOMContentLoaded', updateCartCount);
