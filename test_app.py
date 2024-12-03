import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
from app import app
from database import students_collection

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    """
    Clean the students collection before each test to ensure test isolation.
    """
    students_collection.delete_many({})
    yield
    students_collection.delete_many({})

def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Test User",
            "age": 20,
            "address": {"country": "India", "city": "Delhi"}
        },
    )
    assert response.status_code == 201
    assert "id" in response.json()
    inserted_id = response.json()["id"]
    assert ObjectId.is_valid(inserted_id)

def test_list_students():
    # Add a student to list
    client.post(
        "/students",
        json={
            "name": "List User",
            "age": 30,
            "address": {"country": "India", "city": "Delhi"}
        },
    )
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0

def test_fetch_student():
    post_response = client.post(
        "/students",
        json={
            "name": "Fetch User",
            "age": 22,
            "address": {"country": "USA", "city": "San Francisco"}
        },
    )
    student_id = post_response.json()["id"]

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fetch User"
    assert response.json()["address"]["city"] == "San Francisco"

def test_update_student():
    post_response = client.post(
        "/students",
        json={
            "name": "Update User",
            "age": 24,
            "address": {"country": "UK", "city": "London"}
        },
    )
    student_id = post_response.json()["id"]

    response = client.patch(f"/students/{student_id}", json={"age": 25})
    assert response.status_code == 204

    fetch_response = client.get(f"/students/{student_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["age"] == 25

def test_delete_student():
    post_response = client.post(
        "/students",
        json={
            "name": "Delete User",
            "age": 26,
            "address": {"country": "Canada", "city": "Vancouver"}
        },
    )
    student_id = post_response.json()["id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 200

    fetch_response = client.get(f"/students/{student_id}")
    assert fetch_response.status_code == 404
