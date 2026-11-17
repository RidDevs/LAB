"""
Catalog Microservice (Port 5001)
Responsibilities:
- Maintain product catalog (name, price, stock).
- Handle product queries and inventory deductions/restocks.
- Integrated Swagger UI documentation.
"""

from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Catalog Microservice API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": "Product catalog and inventory management service."
}
swagger = Swagger(app)

# Isolated Database for Catalog Service
products = {
    1: {"id": 1, "name": "Mechanical Keyboard", "price": 89.99, "stock": 15},
    2: {"id": 2, "name": "Wireless Mouse", "price": 45.50, "stock": 30},
    3: {"id": 3, "name": "UltraWide Monitor", "price": 399.99, "stock": 5},
}
next_product_id = 4


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
    return jsonify({"service": "Catalog Service", "status": "running", "port": 5001, "docs": "/apidocs/"}), 200


@app.route("/products", methods=["GET"])
def get_products():
    """
    Get all catalog products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products in catalog
    """
    return jsonify(list(products.values())), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Get product details by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID of the product
    responses:
      200:
        description: Product details
      404:
        description: Product not found
    """
    product = products.get(product_id)
    if not product:
        return jsonify({"error": f"Product {product_id} not found"}), 404
    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def add_product():
    """
    Add a new product to catalog
    ---
    tags:
      - Products
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - price
          properties:
            name:
              type: string
              example: "Gaming Headset"
            price:
              type: number
              example: 59.99
            stock:
              type: integer
              example: 25
    responses:
      201:
        description: Product created successfully
      400:
        description: Invalid request data
    """
    global next_product_id
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Missing 'name' or 'price'"}), 400

    try:
        price = float(data["price"])
        stock = int(data.get("stock", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price or stock"}), 400

    if price < 0 or stock < 0:
        return jsonify({"error": "Price and stock must be non-negative"}), 400

    product = {
        "id": next_product_id,
        "name": data["name"].strip(),
        "price": round(price, 2),
        "stock": stock,
    }
    products[next_product_id] = product
    next_product_id += 1
    return jsonify(product), 201


@app.route("/products/<int:product_id>/deduct", methods=["POST"])
def deduct_stock(product_id):
    """
    Deduct stock for an order
    ---
    tags:
      - Inventory
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            quantity:
              type: integer
              example: 2
    responses:
      200:
        description: Stock successfully deducted
      400:
        description: Insufficient stock or invalid quantity
      404:
        description: Product not found
    """
    data = request.get_json() or {}
    quantity = data.get("quantity", 1)

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be an integer"}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    product = products.get(product_id)
    if not product:
        return jsonify({"error": f"Product {product_id} not found"}), 404

    if product["stock"] < quantity:
        return jsonify({
            "error": "Insufficient stock",
            "available": product["stock"],
            "requested": quantity
        }), 400

    product["stock"] -= quantity
    return jsonify({
        "message": "Stock deducted successfully",
        "product_id": product_id,
        "remaining_stock": product["stock"]
    }), 200


@app.route("/products/<int:product_id>/restock", methods=["POST"])
def restock(product_id):
    """
    Restock inventory (compensation rollback)
    ---
    tags:
      - Inventory
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            quantity:
              type: integer
              example: 2
    responses:
      200:
        description: Stock restored
      404:
        description: Product not found
    """
    data = request.get_json() or {}
    quantity = int(data.get("quantity", 1))

    product = products.get(product_id)
    if not product:
        return jsonify({"error": f"Product {product_id} not found"}), 404

    product["stock"] += quantity
    return jsonify({
        "message": "Stock restored",
        "product_id": product_id,
        "current_stock": product["stock"]
    }), 200


if __name__ == "__main__":
    print("Starting Catalog Service on port 5001 (Swagger: http://127.0.0.1:5001/apidocs/)...")
    app.run(host="0.0.0.0", port=5001, debug=True)
