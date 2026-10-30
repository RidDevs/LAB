"""
End-to-End Integration Tests for Microservices Architecture:
Tests isolated endpoints for Catalog, Cart, and Discount, and tests
cross-service orchestration in Order Service using Flask test clients.
"""

import pytest
from unittest.mock import patch
from services.catalog_service.app import app as catalog_app, products
from services.cart_service.app import app as cart_app, carts
from services.discount_service.app import app as discount_app, discounts
from services.order_service.app import app as order_app, orders


@pytest.fixture
def catalog_client():
    catalog_app.config["TESTING"] = True
    with catalog_app.test_client() as client:
        yield client


@pytest.fixture
def cart_client():
    cart_app.config["TESTING"] = True
    carts.clear()
    with cart_app.test_client() as client:
        yield client


@pytest.fixture
def discount_client():
    discount_app.config["TESTING"] = True
    with discount_app.test_client() as client:
        yield client


@pytest.fixture
def order_client():
    order_app.config["TESTING"] = True
    orders.clear()
    with order_app.test_client() as client:
        yield client


# ==============================================================================
# 1. CATALOG SERVICE TESTS
# ==============================================================================
def test_catalog_service(catalog_client):
    # Get all products
    res = catalog_client.get("/products")
    assert res.status_code == 200
    assert len(res.get_json()) >= 3

    # Add a product
    res = catalog_client.post("/products", json={"name": "Webcam HD", "price": 49.99, "stock": 10})
    assert res.status_code == 201
    pid = res.get_json()["id"]

    # Deduct stock
    deduct_res = catalog_client.post(f"/products/{pid}/deduct", json={"quantity": 3})
    assert deduct_res.status_code == 200
    assert deduct_res.get_json()["remaining_stock"] == 7

    # Deduct more than available stock
    fail_res = catalog_client.post(f"/products/{pid}/deduct", json={"quantity": 100})
    assert fail_res.status_code == 400


# ==============================================================================
# 2. CART SERVICE TESTS
# ==============================================================================
def test_cart_service(cart_client):
    # Add to cart
    res = cart_client.post("/cart/101/items", json={"product_id": 1, "quantity": 2})
    assert res.status_code == 200
    assert res.get_json()["quantity_in_cart"] == 2

    # View cart
    view_res = cart_client.get("/cart/101")
    assert view_res.status_code == 200
    assert len(view_res.get_json()["items"]) == 1

    # Clear cart
    del_res = cart_client.delete("/cart/101")
    assert del_res.status_code == 200
    empty_res = cart_client.get("/cart/101")
    assert len(empty_res.get_json()["items"]) == 0


# ==============================================================================
# 3. DISCOUNT SERVICE TESTS
# ==============================================================================
def test_discount_service(discount_client):
    # Apply valid percentage discount (SAVE10 = 10%)
    res = discount_client.post("/discounts/apply", json={"coupon_code": "SAVE10", "subtotal": 200.0})
    assert res.status_code == 200
    data = res.get_json()
    assert data["valid"] is True
    assert data["discount_amount"] == 20.0
    assert data["final_total"] == 180.0

    # Apply flat discount with minimum order unmet
    flat_fail = discount_client.post("/discounts/apply", json={"coupon_code": "FLAT20", "subtotal": 30.0})
    assert flat_fail.status_code == 400


# ==============================================================================
# 4. ORDER SERVICE (Cross-Service Checkout Orchestration)
# ==============================================================================
def test_order_service_checkout(order_client):
    # Mock inter-service HTTP calls made by Order Service
    def mock_requests_get(url, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json = json_data
                self.status_code = status_code

            def json(self):
                return self._json

        if "/cart/1" in url:
            return MockResponse({"user_id": 1, "items": [{"product_id": 1, "quantity": 2}]})
        elif "/products/1" in url:
            return MockResponse({"id": 1, "name": "Mechanical Keyboard", "price": 100.0, "stock": 10})
        return MockResponse({"error": "not found"}, 404)

    def mock_requests_post(url, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code=200):
                self._json = json_data
                self.status_code = status_code

            def json(self):
                return self._json

        if "/discounts/apply" in url:
            return MockResponse({"valid": True, "discount_amount": 20.0, "final_total": 180.0})
        elif "/deduct" in url:
            return MockResponse({"message": "Stock deducted", "remaining_stock": 8})
        return MockResponse({"error": "failed"}, 400)

    def mock_requests_delete(url, *args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"message": "cleared"}
        return MockResponse()

    with patch("services.order_service.app.requests.get", side_effect=mock_requests_get), \
         patch("services.order_service.app.requests.post", side_effect=mock_requests_post), \
         patch("services.order_service.app.requests.delete", side_effect=mock_requests_delete):

        res = order_client.post("/orders/checkout", json={"user_id": 1, "coupon_code": "SAVE10"})
        assert res.status_code == 201
        data = res.get_json()["order"]
        assert data["order_id"] == 1
        assert data["subtotal"] == 200.0
        assert data["discount_amount"] == 20.0
        assert data["final_total"] == 180.0
        assert data["status"] == "CONFIRMED"
