import pytest
from services.frontend_service.app import app as frontend_app


@pytest.fixture
def frontend_client():
    frontend_app.config["TESTING"] = True
    with frontend_app.test_client() as client:
        yield client


def test_frontend_home(frontend_client):
    res = frontend_client.get("/")
    assert res.status_code == 200
    assert b"E-Commerce Microservices Hub" in res.data
    assert b"Catalog API" in res.data
    assert b"Cart API" in res.data
    assert b"Discount API" in res.data
    assert b"Order API" in res.data

