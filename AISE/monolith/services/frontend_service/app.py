"""
Frontend UI Microservice (Port 5000)
Responsibilities:
- Serves the Web Storefront & Management Dashboard for the E-Commerce Microservices.
- Acts as a Web UI / Backend-For-Frontend (BFF) gateway connecting Catalog, Cart, Discount, and Order services.
- Provides interactive UI for shopping, checkout, and links to all microservices' Swagger UIs.
"""

import os
import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Microservices URLs
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://127.0.0.1:5001")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://127.0.0.1:5002")
DISCOUNT_SERVICE_URL = os.getenv("DISCOUNT_SERVICE_URL", "http://127.0.0.1:5003")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://127.0.0.1:5004")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E-Commerce Microservices Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <style>
    body { background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .hero-header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem 0; margin-bottom: 2rem; border-radius: 0 0 1rem 1rem; }
    .card { border: none; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08); transition: transform 0.15s ease-in-out; }
    .card:hover { transform: translateY(-2px); }
    .badge-service { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .swagger-btn { font-size: 0.8rem; }
  </style>
</head>
<body>

  <!-- Header -->
  <div class="hero-header shadow-sm">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h2 class="fw-bold mb-1"><i class="bi bi-box-seam me-2"></i>E-Commerce Microservices Hub</h2>
          <p class="mb-0 opacity-75">Frontend UI Service (Port 5000) orchestrating 4 independent backend microservices</p>
        </div>
        <div>
          <span class="badge bg-light text-dark px-3 py-2 rounded-pill">
            <i class="bi bi-person-circle me-1"></i> Current User ID: <strong>101</strong>
          </span>
        </div>
      </div>
    </div>
  </div>

  <div class="container mb-5">

    <!-- Alert / Status notifications -->
    <div id="alertBox" class="alert d-none" role="alert"></div>

    <div class="row g-4">

      <!-- LEFT COLUMN: Product Catalog -->
      <div class="col-lg-7">
        <div class="card h-100">
          <div class="card-header bg-white border-0 pt-3 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0 text-primary"><i class="bi bi-shop me-2"></i>Product Catalog <span class="badge bg-primary-subtle text-primary badge-service">Port 5001</span></h5>
            <button class="btn btn-sm btn-outline-secondary" onclick="loadCatalog()"><i class="bi bi-arrow-clockwise"></i> Refresh</button>
          </div>
          <div class="card-body">
            <div id="catalogList" class="row g-3">
              <div class="text-center text-muted py-4"><span class="spinner-border spinner-border-sm me-2"></span>Loading catalog...</div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: Cart & Checkout -->
      <div class="col-lg-5">
        
        <!-- Cart Card -->
        <div class="card mb-4">
          <div class="card-header bg-white border-0 pt-3 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0 text-success"><i class="bi bi-cart3 me-2"></i>Shopping Cart <span class="badge bg-success-subtle text-success badge-service">Port 5002</span></h5>
            <button class="btn btn-sm btn-outline-danger" onclick="clearCart()"><i class="bi bi-trash"></i> Clear</button>
          </div>
          <div class="card-body">
            <div id="cartContent">
              <div class="text-center text-muted py-3">Your cart is empty.</div>
            </div>
          </div>
        </div>

        <!-- Checkout Card -->
        <div class="card mb-4">
          <div class="card-header bg-white border-0 pt-3 pb-0">
            <h5 class="fw-bold mb-0 text-danger"><i class="bi bi-credit-card me-2"></i>Order Checkout <span class="badge bg-danger-subtle text-danger badge-service">Port 5004</span></h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label small fw-semibold">Discount Voucher Code <span class="badge bg-warning-subtle text-dark badge-service">Port 5003</span></label>
              <div class="input-group">
                <input type="text" id="couponInput" class="form-control" placeholder="e.g. SAVE10, FLAT20, SUPER50">
                <button class="btn btn-outline-secondary" type="button" onclick="testCoupon()"><i class="bi bi-check-circle"></i> Validate</button>
              </div>
              <small class="text-muted">Available coupons: <code>SAVE10</code> (10% off), <code>FLAT20</code> ($20 off orders > $50), <code>SUPER50</code> (50% off > $100)</small>
            </div>
            <button class="btn btn-danger w-100 py-2 fw-semibold" onclick="placeOrder()">
              <i class="bi bi-check-all me-1"></i> Place Order (Distributed Checkout)
            </button>
          </div>
        </div>

        <!-- Placed Orders History -->
        <div class="card">
          <div class="card-header bg-white border-0 pt-3 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0 text-dark"><i class="bi bi-receipt me-2"></i>Recent Orders</h5>
            <button class="btn btn-sm btn-outline-secondary" onclick="loadOrders()"><i class="bi bi-arrow-clockwise"></i></button>
          </div>
          <div class="card-body">
            <div id="ordersList" class="small text-muted py-2">No orders placed yet.</div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <script>
    const USER_ID = 101;

    function showAlert(msg, type='info') {
      const box = document.getElementById('alertBox');
      box.className = `alert alert-${type} shadow-sm`;
      box.innerHTML = msg;
      box.classList.remove('d-none');
      setTimeout(() => { box.classList.add('d-none'); }, 5000);
    }

    async function loadCatalog() {
      try {
        const res = await fetch('/api/products');
        const prods = await res.json();
        const container = document.getElementById('catalogList');
        if (!prods.length) {
          container.innerHTML = '<div class="col-12 text-muted">No products available.</div>';
          return;
        }
        container.innerHTML = prods.map(p => `
          <div class="col-md-6 col-12">
            <div class="card border p-3 h-100 bg-light-subtle">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h6 class="fw-bold mb-0 text-truncate" style="max-width: 170px;">${p.name}</h6>
                <span class="badge ${p.stock > 0 ? 'bg-success' : 'bg-secondary'}">${p.stock} in stock</span>
              </div>
              <div class="h5 fw-bold text-dark mb-3">$${p.price.toFixed(2)}</div>
              <button class="btn btn-sm btn-primary w-100" onclick="addToCart(${p.id})" ${p.stock <= 0 ? 'disabled' : ''}>
                <i class="bi bi-cart-plus me-1"></i> Add to Cart
              </button>
            </div>
          </div>
        `).join('');
      } catch (err) {
        document.getElementById('catalogList').innerHTML = '<div class="col-12 text-danger">Failed to connect to Catalog Service (Port 5001).</div>';
      }
    }

    async function loadCart() {
      try {
        const res = await fetch(`/api/cart/${USER_ID}`);
        const data = await res.json();
        const container = document.getElementById('cartContent');
        if (!data.items || !data.items.length) {
          container.innerHTML = '<div class="text-center text-muted py-3">Your cart is empty.</div>';
          return;
        }
        container.innerHTML = `
          <ul class="list-group list-group-flush mb-2">
            ${data.items.map(i => `
              <li class="list-group-item d-flex justify-content-between align-items-center px-0">
                <div>
                  <span class="fw-medium">Product #${i.product_id}</span>
                  <small class="text-muted d-block">Qty: ${i.quantity}</small>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${i.product_id})">
                  <i class="bi bi-x"></i>
                </button>
              </li>
            `).join('')}
          </ul>
          <div class="small text-muted text-end">Total Items: <strong>${data.item_count}</strong></div>
        `;
      } catch (err) {
        document.getElementById('cartContent').innerHTML = '<div class="text-danger small">Failed to reach Cart Service (Port 5002).</div>';
      }
    }

    async function addToCart(productId) {
      try {
        const res = await fetch(`/api/cart/${USER_ID}/items`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ product_id: productId, quantity: 1 })
        });
        const data = await res.json();
        if (res.ok) {
          showAlert(`Added item to cart!`, 'success');
          loadCart();
        } else {
          showAlert(data.error || 'Failed to add item', 'danger');
        }
      } catch (err) {
        showAlert('Could not reach Cart Service', 'danger');
      }
    }

    async function removeFromCart(productId) {
      try {
        await fetch(`/api/cart/${USER_ID}/items/${productId}`, { method: 'DELETE' });
        loadCart();
      } catch (err) {
        showAlert('Failed to remove item', 'danger');
      }
    }

    async function clearCart() {
      try {
        await fetch(`/api/cart/${USER_ID}`, { method: 'DELETE' });
        showAlert('Cart cleared', 'info');
        loadCart();
      } catch (err) {
        showAlert('Failed to clear cart', 'danger');
      }
    }

    async function testCoupon() {
      const code = document.getElementById('couponInput').value.trim();
      if (!code) { showAlert('Please enter a coupon code', 'warning'); return; }
      try {
        const res = await fetch(`/api/discounts/${code}`);
        const data = await res.json();
        if (res.ok) {
          showAlert(`Coupon <strong>${data.code}</strong> is active! (${data.value}${data.type === 'PERCENT' ? '%' : '$'} off, min order: $${data.min_order})`, 'success');
        } else {
          showAlert(data.error || 'Invalid coupon', 'warning');
        }
      } catch (err) {
        showAlert('Failed to reach Discount Service', 'danger');
      }
    }

    async function placeOrder() {
      const code = document.getElementById('couponInput').value.trim();
      try {
        const res = await fetch('/api/orders/checkout', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ user_id: USER_ID, coupon_code: code || null })
        });
        const data = await res.json();
        if (res.ok) {
          showAlert(`Order #${data.order.order_id} Confirmed! Total: $${data.order.final_total} (Discount: $${data.order.discount_amount})`, 'success');
          loadCart();
          loadCatalog();
          loadOrders();
        } else {
          showAlert(data.error || 'Checkout failed', 'danger');
        }
      } catch (err) {
        showAlert('Order Service unavailable', 'danger');
      }
    }

    async function loadOrders() {
      try {
        const res = await fetch(`/api/orders/user/${USER_ID}`);
        const list = await res.json();
        const container = document.getElementById('ordersList');
        if (!list.length) {
          container.innerHTML = 'No orders placed yet.';
          return;
        }
        container.innerHTML = list.map(o => `
          <div class="border rounded p-2 mb-2 bg-white">
            <div class="d-flex justify-content-between fw-bold">
              <span>Order #${o.order_id}</span>
              <span class="text-success">$${o.final_total.toFixed(2)}</span>
            </div>
            <div class="text-muted small">Items: ${o.items.length} | Status: <span class="badge bg-success-subtle text-success">${o.status}</span></div>
            ${o.discount_amount > 0 ? `<div class="text-warning small">Coupon: ${o.discount_code} (-$${o.discount_amount})</div>` : ''}
          </div>
        `).join('');
      } catch (err) {
        document.getElementById('ordersList').innerHTML = '<div class="text-danger">Failed to fetch orders.</div>';
      }
    }

    // Initial loading
    loadCatalog();
    loadCart();
    loadOrders();
  </script>
</body>
</html>
"""

# ==============================================================================
# BFF / PROXY ENDPOINTS (Connects Frontend UI directly to Backend Services)
# ==============================================================================
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/products", methods=["GET"])
def proxy_products():
    res = requests.get(f"{CATALOG_SERVICE_URL}/products", timeout=3)
    return jsonify(res.json()), res.status_code


@app.route("/api/cart/<int:user_id>", methods=["GET", "DELETE"])
def proxy_cart(user_id):
    if request.method == "GET":
        res = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=3)
    else:
        res = requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=3)
    return jsonify(res.json()), res.status_code


@app.route("/api/cart/<int:user_id>/items", methods=["POST"])
def proxy_add_cart(user_id):
    res = requests.post(f"{CART_SERVICE_URL}/cart/{user_id}/items", json=request.get_json(), timeout=3)
    return jsonify(res.json()), res.status_code


@app.route("/api/cart/<int:user_id>/items/<int:product_id>", methods=["DELETE"])
def proxy_remove_cart(user_id, product_id):
    res = requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}/items/{product_id}", timeout=3)
    return jsonify(res.json()), res.status_code


@app.route("/api/discounts/<string:code>", methods=["GET"])
def proxy_discount(code):
    res = requests.get(f"{DISCOUNT_SERVICE_URL}/discounts/{code}", timeout=3)
    return jsonify(res.json()), res.status_code


@app.route("/api/orders/checkout", methods=["POST"])
def proxy_checkout():
    res = requests.post(f"{ORDER_SERVICE_URL}/orders/checkout", json=request.get_json(), timeout=5)
    return jsonify(res.json()), res.status_code


@app.route("/api/orders/user/<int:user_id>", methods=["GET"])
def proxy_user_orders(user_id):
    res = requests.get(f"{ORDER_SERVICE_URL}/orders/user/{user_id}", timeout=3)
    return jsonify(res.json()), res.status_code


if __name__ == "__main__":
    print("Starting Frontend UI Service on port 5000 (UI: http://127.0.0.1:5000)...")
    app.run(host="0.0.0.0", port=5000, debug=True)

