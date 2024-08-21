from uuid import uuid4

from fastapi.testclient import TestClient

from app import app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)


def test_create_order():
    order_data = {
        "product": "example_item",
        "status": "created",
        "quantity": 1,
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["item"] == "example_item"
    assert response_json["quantity"] == 1
    assert response_json["status"] == "created"
    assert "id" in response_json
    assert "created" in response_json


def test_get_orders():
    # Send a GET request to the /items/ endpoint
    response = client.get("/orders")

    # Check that the status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response JSON is what we expect
    assert response.json() == [{"id": "foo"}, {"id": "bar"}]


def test_delete_order():
    # Create a UUID for testing
    test_order_id = uuid4()

    # Send a DELETE request to the /orders/{order_id} endpoint
    response = client.delete(f"/orders/{test_order_id}")

    # Check that the status code is 204 (No Content)
    assert response.status_code == 204

    # Check that the response content is empty
    assert response.content == b""
