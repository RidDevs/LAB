"""
Shopping Cart Microservice (Port 5002)
Responsibilities:
- Manage user shopping carts (add, update, delete, clear).
- Integrated Swagger UI documentation.
"""

import os
import requests
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Shopping Cart Microservice API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": "Customer shopping cart management service."
}
swagger = Swagger(app)

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://127.0.0.1:5001")

# Isolated Database for Cart Service: { user_id: { product_id: quantity } }
carts = {}


@app.route("/", methods=["GET"])
def health():
    """
    Service Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: Service status and port
    """
    return jsonify({"service": "Shopping Cart Service", "status": "running", "port": 5002, "docs": "/apidocs/"}), 200


@app.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    """
    Get user shopping cart items
    ---
    tags:
      - Cart
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of user
    responses:
      200:
        description: Cart items and total count
    """
    user_cart = carts.get(user_id, {})
    items = [{"product_id": pid, "quantity": qty} for pid, qty in user_cart.items()]
    return jsonify({
        "user_id": user_id,
        "items": items,
        "item_count": sum(user_cart.values())
    }), 200


@app.route("/cart/<int:user_id>/items", methods=["POST"])
def add_to_cart(user_id):
    """
    Add item to cart or increment quantity
    ---
    tags:
      - Cart
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - product_id
          properties:
            product_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 1
    responses:
      200:
        description: Item added to cart
      400:
        description: Invalid request data
      404:
        description: Product not found in catalog
    """
    data = request.get_json()
    if not data or "product_id" not in data:
        return jsonify({"error": "Missing 'product_id'"}), 400

    try:
        product_id = int(data["product_id"])
        quantity = int(data.get("quantity", 1))
    except (ValueError, TypeError):
        return jsonify({"error": "product_id and quantity must be integers"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    # Optional verification with Catalog Service over HTTP
    try:
        cat_resp = requests.get(f"{CATALOG_SERVICE_URL}/products/{product_id}", timeout=2)
        if cat_resp.status_code == 404:
            return jsonify({"error": f"Product {product_id} does not exist in Catalog"}), 404
    except requests.RequestException:
        pass

    if user_id not in carts:
        carts[user_id] = {}

    carts[user_id][product_id] = carts[user_id].get(product_id, 0) + quantity

    return jsonify({
        "message": "Item added to cart",
        "user_id": user_id,
        "product_id": product_id,
        "quantity_in_cart": carts[user_id][product_id]
    }), 200


@app.route("/cart/<int:user_id>/items/<int:product_id>", methods=["DELETE"])
def remove_from_cart(user_id, product_id):
    """
    Remove product from user cart
    ---
    tags:
      - Cart
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Item removed
      404:
        description: Item not in cart
    """
    if user_id not in carts or product_id not in carts[user_id]:
        return jsonify({"error": "Item not found in cart"}), 404

    del carts[user_id][product_id]
    return jsonify({"message": f"Product {product_id} removed from cart"}), 200


@app.route("/cart/<int:user_id>", methods=["DELETE"])
def clear_cart(user_id):
    """
    Clear all items from user cart
    ---
    tags:
      - Cart
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cart cleared
    """
    if user_id in carts:
        carts[user_id] = {}
    return jsonify({"message": f"Cart for user {user_id} cleared"}), 200


if __name__ == "__main__":
    print("Starting Shopping Cart Service on port 5002 (Swagger: http://127.0.0.1:5002/apidocs/)...")
    app.run(host="0.0.0.0", port=5002, debug=True)
