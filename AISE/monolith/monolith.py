"""
Monolithic E-commerce Application
Contains all four core services combined into a single application:
1. User Service: User account management and lookup
2. Product Service: Product catalog and inventory management
3. Order Service: Order creation, stock reservation, and history
4. Payment Service: Payment processing and status tracking
"""

from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# ==============================================================================
# CENTRALIZED SHARED DATA STORE (In-Memory Monolith Database)
# ==============================================================================
db = {
    "users": {
        1: {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob Jones", "email": "bob@example.com"},
    },
    "products": {
        1: {"id": 1, "name": "Mechanical Keyboard", "price": 89.99, "stock": 15},
        2: {"id": 2, "name": "Wireless Mouse", "price": 45.50, "stock": 30},
        3: {"id": 3, "name": "UltraWide Monitor", "price": 399.99, "stock": 5},
    },
    "orders": {},
    "payments": {},
}

id_counters = {
    "users": 3,
    "products": 4,
    "orders": 1,
    "payments": 1,
}


# ==============================================================================
# SERVICE 1: USER SERVICE (User Management)
# ==============================================================================
@app.route("/users", methods=["GET"])
def get_users():
    """Retrieve all registered users."""
    return jsonify(list(db["users"].values())), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieve a single user by ID."""
    user = db["users"].get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/users", methods=["POST"])
def create_user():
    """Register a new user."""
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'email'"}), 400

    name = data["name"].strip()
    email = data["email"].strip()

    if not name or not email:
        return jsonify({"error": "Fields 'name' and 'email' cannot be empty"}), 400

    # Ensure email uniqueness
    for user in db["users"].values():
        if user["email"].lower() == email.lower():
            return jsonify({"error": "User with this email already exists"}), 409

    user_id = id_counters["users"]
    id_counters["users"] += 1

    new_user = {"id": user_id, "name": name, "email": email}
    db["users"][user_id] = new_user
    return jsonify(new_user), 201


# ==============================================================================
# SERVICE 2: PRODUCT SERVICE (Product Catalog & Inventory)
# ==============================================================================
@app.route("/products", methods=["GET"])
def get_products():
    """Retrieve all catalog products."""
    return jsonify(list(db["products"].values())), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieve a product by ID."""
    product = db["products"].get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def create_product():
    """Add a new product to inventory."""
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Missing required fields: 'name' and 'price'"}), 400

    name = data["name"].strip()
    try:
        price = float(data["price"])
        stock = int(data.get("stock", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Price must be a number and stock must be an integer"}), 400

    if price < 0 or stock < 0:
        return jsonify({"error": "Price and stock must be non-negative"}), 400

    product_id = id_counters["products"]
    id_counters["products"] += 1

    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    }
    db["products"][product_id] = new_product
    return jsonify(new_product), 201


# ==============================================================================
# SERVICE 3: ORDER SERVICE (Order Creation & History)
# ==============================================================================
@app.route("/orders", methods=["GET"])
def get_orders():
    """Retrieve all orders."""
    return jsonify(list(db["orders"].values())), 200


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Retrieve order details by ID."""
    order = db["orders"].get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200


@app.route("/users/<int:user_id>/orders", methods=["GET"])
def get_user_orders(user_id):
    """Retrieve orders placed by a specific user."""
    if user_id not in db["users"]:
        return jsonify({"error": "User not found"}), 404
    user_orders = [o for o in db["orders"].values() if o["user_id"] == user_id]
    return jsonify(user_orders), 200


@app.route("/orders", methods=["POST"])
def create_order():
    """
    Create an order.
    In the monolith, cross-module communication happens through direct in-memory calls:
    1. Validates user existence with User Service domain.
    2. Validates product existence and stock with Product Service domain.
    3. Mutates inventory directly and creates the order.
    """
    data = request.get_json()
    if not data or "user_id" not in data or "product_id" not in data:
        return jsonify({"error": "Missing required fields: 'user_id' and 'product_id'"}), 400

    user_id = data["user_id"]
    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    # Cross-service verification: User domain
    if user_id not in db["users"]:
        return jsonify({"error": "User does not exist"}), 404

    # Cross-service verification: Product domain
    product = db["products"].get(product_id)
    if not product:
        return jsonify({"error": "Product does not exist"}), 404

    # Inventory check
    if product["stock"] < quantity:
        return jsonify({"error": f"Insufficient stock. Only {product['stock']} available."}), 400

    # Monolithic in-memory transaction: deduct inventory immediately
    product["stock"] -= quantity

    order_id = id_counters["orders"]
    id_counters["orders"] += 1

    total_price = round(product["price"] * quantity, 2)

    order = {
        "id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "product_name": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "total_price": total_price,
        "status": "PENDING_PAYMENT",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    db["orders"][order_id] = order
    return jsonify(order), 201


# ==============================================================================
# SERVICE 4: PAYMENT SERVICE (Billing & Transactions)
# ==============================================================================
@app.route("/payments", methods=["GET"])
def get_payments():
    """Retrieve all payment records."""
    return jsonify(list(db["payments"].values())), 200


@app.route("/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    """Retrieve a payment transaction by ID."""
    payment = db["payments"].get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment), 200


@app.route("/payments", methods=["POST"])
def process_payment():
    """
    Process payment for an existing pending order.
    In the monolith, Payment Service directly looks up and updates the Order domain state.
    """
    data = request.get_json()
    if not data or "order_id" not in data or "amount" not in data:
        return jsonify({"error": "Missing required fields: 'order_id' and 'amount'"}), 400

    order_id = data["order_id"]
    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a numeric value"}), 400

    order = db["orders"].get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order["status"] == "PAID":
        return jsonify({"error": "Order is already paid"}), 400

    if amount < order["total_price"]:
        return jsonify({
            "error": "Insufficient payment amount",
            "required": order["total_price"],
            "provided": amount
        }), 400

    payment_id = id_counters["payments"]
    id_counters["payments"] += 1

    payment = {
        "id": payment_id,
        "order_id": order_id,
        "amount": amount,
        "status": "SUCCESS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    db["payments"][payment_id] = payment

    # Direct monolithic state update on Order domain
    order["status"] = "PAID"
    order["payment_id"] = payment_id

    return jsonify({
        "message": "Payment processed successfully",
        "payment": payment,
        "order": order
    }), 200


# ==============================================================================
# APPLICATION HEALTH / OVERVIEW ROUTE
# ==============================================================================
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "application": "Monolithic E-Commerce Application",
        "status": "running",
        "services": [
            "User Service (/users)",
            "Product Service (/products)",
            "Order Service (/orders)",
            "Payment Service (/payments)"
        ]
    }), 200


if __name__ == "__main__":
    print("==================================================")
    print(" Starting Monolithic E-Commerce Application...")
    print(" Core Services Loaded:")
    print("   1. User Service")
    print("   2. Product Service")
    print("   3. Order Service")
    print("   4. Payment Service")
    print(" Running at http://127.0.0.1:5000")
    print("==================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)

