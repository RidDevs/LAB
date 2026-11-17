"""
Discount Microservice (Port 5003)
Responsibilities:
- Manage discount coupons and promotions.
- Validate coupon codes and compute discounts based on order subtotal.
- Integrated Swagger UI documentation.
"""

from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Discount Microservice API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": "Coupons, promotions, and discount calculation service."
}
swagger = Swagger(app)

# Isolated Database for Discount Service
discounts = {
    "SAVE10": {
        "code": "SAVE10",
        "type": "PERCENT",
        "value": 10.0,
        "min_order": 0.0,
    },
    "FLAT20": {
        "code": "FLAT20",
        "type": "FLAT",
        "value": 20.0,
        "min_order": 50.0,
    },
    "SUPER50": {
        "code": "SUPER50",
        "type": "PERCENT",
        "value": 50.0,
        "min_order": 100.0,
    },
}


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
    return jsonify({"service": "Discount Service", "status": "running", "port": 5003, "docs": "/apidocs/"}), 200


@app.route("/discounts", methods=["GET"])
def get_discounts():
    """
    Retrieve all active discounts
    ---
    tags:
      - Discounts
    responses:
      200:
        description: List of available discount codes
    """
    return jsonify(list(discounts.values())), 200


@app.route("/discounts/<string:code>", methods=["GET"])
def get_discount(code):
    """
    Get discount coupon details by code
    ---
    tags:
      - Discounts
    parameters:
      - name: code
        in: path
        type: string
        required: true
        example: SAVE10
    responses:
      200:
        description: Coupon details
      404:
        description: Discount code not found
    """
    discount = discounts.get(code.upper())
    if not discount:
        return jsonify({"error": f"Discount code '{code}' not found"}), 404
    return jsonify(discount), 200


@app.route("/discounts", methods=["POST"])
def create_discount():
    """
    Create a new discount code
    ---
    tags:
      - Discounts
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - code
            - type
            - value
          properties:
            code:
              type: string
              example: FESTIVE25
            type:
              type: string
              enum: ["PERCENT", "FLAT"]
              example: "PERCENT"
            value:
              type: number
              example: 25.0
            min_order:
              type: number
              example: 50.0
    responses:
      201:
        description: Coupon created
      400:
        description: Invalid request parameters
    """
    data = request.get_json()
    if not data or "code" not in data or "type" not in data or "value" not in data:
        return jsonify({"error": "Missing required fields: 'code', 'type', 'value'"}), 400

    code = data["code"].strip().upper()
    disc_type = data["type"].strip().upper()
    if disc_type not in ["PERCENT", "FLAT"]:
        return jsonify({"error": "Type must be 'PERCENT' or 'FLAT'"}), 400

    try:
        val = float(data["value"])
        min_order = float(data.get("min_order", 0.0))
    except (ValueError, TypeError):
        return jsonify({"error": "Value and min_order must be numeric"}), 400

    if disc_type == "PERCENT" and (val <= 0 or val > 100):
        return jsonify({"error": "Percentage value must be between 1 and 100"}), 400

    discounts[code] = {
        "code": code,
        "type": disc_type,
        "value": val,
        "min_order": min_order,
    }
    return jsonify(discounts[code]), 201


@app.route("/discounts/apply", methods=["POST"])
def apply_discount():
    """
    Validate and calculate discount for an order subtotal
    ---
    tags:
      - Discounts
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - coupon_code
            - subtotal
          properties:
            coupon_code:
              type: string
              example: "SAVE10"
            subtotal:
              type: number
              example: 100.0
    responses:
      200:
        description: Discount calculation result
      400:
        description: Subtotal does not meet minimum threshold
      404:
        description: Invalid coupon code
    """
    data = request.get_json()
    if not data or "coupon_code" not in data or "subtotal" not in data:
        return jsonify({"error": "Missing 'coupon_code' or 'subtotal'"}), 400

    code = data["coupon_code"].strip().upper()
    try:
        subtotal = float(data["subtotal"])
    except (ValueError, TypeError):
        return jsonify({"error": "Subtotal must be a valid number"}), 400

    coupon = discounts.get(code)
    if not coupon:
        return jsonify({
            "valid": False,
            "error": f"Invalid or expired coupon code: '{code}'"
        }), 404

    if subtotal < coupon["min_order"]:
        return jsonify({
            "valid": False,
            "error": f"Minimum order amount of ${coupon['min_order']:.2f} required for coupon '{code}'"
        }), 400

    if coupon["type"] == "PERCENT":
        discount_amount = round(subtotal * (coupon["value"] / 100.0), 2)
    else:  # FLAT
        discount_amount = round(min(coupon["value"], subtotal), 2)

    final_total = round(max(0.0, subtotal - discount_amount), 2)

    return jsonify({
        "valid": True,
        "code": code,
        "type": coupon["type"],
        "discount_amount": discount_amount,
        "original_subtotal": subtotal,
        "final_total": final_total
    }), 200


if __name__ == "__main__":
    print("Starting Discount Service on port 5003 (Swagger: http://127.0.0.1:5003/apidocs/)...")
    app.run(host="0.0.0.0", port=5003, debug=True)
