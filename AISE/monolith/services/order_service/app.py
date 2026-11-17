"""
Order Microservice (Port 5004)
Responsibilities:
- Orchestrate distributed order checkout.
- Communicates over HTTP with Catalog Service, Shopping Cart Service, and Discount Service.
- Integrated Swagger UI documentation.
"""

import os
from datetime import datetime, timezone
import requests
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Order Orchestrator Microservice API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": "Order lifecycle, history, and distributed checkout orchestration service."
}
swagger = Swagger(app)

# Configurable Service URLs
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://127.0.0.1:5001")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://127.0.0.1:5002")
DISCOUNT_SERVICE_URL = os.getenv("DISCOUNT_SERVICE_URL", "http://127.0.0.1:5003")

# Isolated Database for Order Service
orders = {}
next_order_id = 1


@app.route("/", methods=["GET"])
def health():
    """
    Service Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: Service status, port, and dependencies
    """
    return jsonify({
        "service": "Order Service",
        "status": "running",
        "port": 5004,
        "docs": "/apidocs/",
        "dependencies": {
            "catalog_service": CATALOG_SERVICE_URL,
            "cart_service": CART_SERVICE_URL,
            "discount_service": DISCOUNT_SERVICE_URL,
        }
    }), 200


@app.route("/orders", methods=["GET"])
def get_orders():
    """
    Retrieve all orders
    ---
    tags:
      - Orders
    responses:
      200:
        description: List of all placed orders
    """
    return jsonify(list(orders.values())), 200


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Get order by ID
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Order record
      404:
        description: Order not found
    """
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": f"Order {order_id} not found"}), 404
    return jsonify(order), 200


@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_user_orders(user_id):
    """
    Get all orders for a specific user
    ---
    tags:
      - Orders
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Orders placed by the user
    """
    user_orders = [o for o in orders.values() if o["user_id"] == user_id]
    return jsonify(user_orders), 200


@app.route("/orders/checkout", methods=["POST"])
def checkout():
    """
    Orchestrated Distributed Checkout
    ---
    tags:
      - Checkout
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: integer
              example: 101
            coupon_code:
              type: string
              example: "SAVE10"
    responses:
      201:
        description: Order placed successfully
      400:
        description: Empty cart, insufficient stock, or invalid coupon
      503:
        description: Downstream microservice unavailable
    """
    global next_order_id
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "Missing 'user_id'"}), 400

    user_id = data["user_id"]
    coupon_code = data.get("coupon_code")

    # Step 1: Fetch Cart from Shopping Cart Service
    try:
        cart_resp = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=3)
    except requests.RequestException as e:
        return jsonify({"error": "Failed to reach Shopping Cart Service", "detail": str(e)}), 503

    if cart_resp.status_code != 200:
        return jsonify({"error": "Failed to retrieve cart"}), cart_resp.status_code

    cart_data = cart_resp.json()
    items = cart_data.get("items", [])
    if not items:
        return jsonify({"error": "Shopping cart is empty. Add items before checking out."}), 400

    # Step 2: Validate Items & Prices with Catalog Service
    order_items = []
    subtotal = 0.0

    for item in items:
        pid = item["product_id"]
        qty = item["quantity"]

        try:
            prod_resp = requests.get(f"{CATALOG_SERVICE_URL}/products/{pid}", timeout=3)
        except requests.RequestException as e:
            return jsonify({"error": f"Failed to reach Catalog Service for product {pid}", "detail": str(e)}), 503

        if prod_resp.status_code != 200:
            return jsonify({"error": f"Product {pid} in cart does not exist in catalog"}), 400

        product = prod_resp.json()
        if product["stock"] < qty:
            return jsonify({
                "error": f"Insufficient stock for '{product['name']}'. Available: {product['stock']}, Requested: {qty}"
            }), 400

        item_subtotal = round(product["price"] * qty, 2)
        subtotal += item_subtotal
        order_items.append({
            "product_id": pid,
            "product_name": product["name"],
            "unit_price": product["price"],
            "quantity": qty,
            "total_price": item_subtotal,
        })

    subtotal = round(subtotal, 2)
    discount_amount = 0.0
    discount_info = None

    # Step 3: Apply Discount from Discount Service (if code provided)
    if coupon_code:
        try:
            disc_resp = requests.post(
                f"{DISCOUNT_SERVICE_URL}/discounts/apply",
                json={"coupon_code": coupon_code, "subtotal": subtotal},
                timeout=3,
            )
        except requests.RequestException as e:
            return jsonify({"error": "Failed to reach Discount Service", "detail": str(e)}), 503

        if disc_resp.status_code != 200:
            err = disc_resp.json().get("error", "Coupon validation failed")
            return jsonify({"error": err}), disc_resp.status_code

        discount_info = disc_resp.json()
        discount_amount = discount_info.get("discount_amount", 0.0)

    final_total = round(max(0.0, subtotal - discount_amount), 2)

    # Step 4: Distributed Inventory Deduction with Compensation Rollback
    deducted_items = []
    for item in order_items:
        try:
            deduct_resp = requests.post(
                f"{CATALOG_SERVICE_URL}/products/{item['product_id']}/deduct",
                json={"quantity": item["quantity"]},
                timeout=3,
            )
            if deduct_resp.status_code != 200:
                for compensated in deducted_items:
                    requests.post(
                        f"{CATALOG_SERVICE_URL}/products/{compensated['product_id']}/restock",
                        json={"quantity": compensated["quantity"]},
                        timeout=2,
                    )
                return jsonify({
                    "error": f"Failed to reserve stock for product {item['product_id']}"
                }), 400

            deducted_items.append(item)
        except requests.RequestException:
            for compensated in deducted_items:
                requests.post(
                    f"{CATALOG_SERVICE_URL}/products/{compensated['product_id']}/restock",
                    json={"quantity": compensated["quantity"]},
                    timeout=2,
                )
            return jsonify({"error": "Stock deduction failed due to network error"}), 503

    # Step 5: Save Confirmed Order in Isolated DB
    order_id = next_order_id
    next_order_id += 1

    order_record = {
        "order_id": order_id,
        "user_id": user_id,
        "items": order_items,
        "subtotal": subtotal,
        "discount_code": coupon_code,
        "discount_amount": discount_amount,
        "final_total": final_total,
        "status": "CONFIRMED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    orders[order_id] = order_record

    # Step 6: Clear Shopping Cart in Cart Service
    try:
        requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}", timeout=2)
    except requests.RequestException:
        pass

    return jsonify({
        "message": "Order placed successfully",
        "order": order_record,
    }), 201


if __name__ == "__main__":
    print("Starting Order Service on port 5004 (Swagger: http://127.0.0.1:5004/apidocs/)...")
    app.run(host="0.0.0.0", port=5004, debug=True)
