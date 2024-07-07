import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
import jwt

client = TestClient(app)

def test_register_user_successfully(db_session):
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john1.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })

    if response.status_code != 201 or "message" not in response.json() or "accessToken" not in response.json()["data"] or "user" not in response.json()["data"]:
        print(response.json())

    assert response.status_code == 201
    assert response.json()["message"] == "Registration successful"
    assert "accessToken" in response.json()["data"]
    assert response.json()["data"]["user"]["firstName"] == "John"
    assert response.json()["data"]["user"]["lastName"] == "Doe"
    assert response.json()["data"]["user"]["email"] == "john1.doe@example.com"




def test_register_user_successfully_with_default_organisation():
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })

    assert response.status_code == 200
    assert response.json()["firstName"] == "John"
    assert response.json()["lastName"] == "Doe"
    assert "accessToken" in response.json()
    assert response.json()["organisation"]["name"] == "John's Organisation"




def test_login_user_successfully():
    response = client.post("/auth/login", json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    if response.status_code != 201 or "email" not in response.json()["data"]["user"] or "accessToken" not in response.json()["data"]:
        print(response.json())

    assert response.status_code == 201
    assert response.json()["data"]["user"]["email"] == "john.doe@example.com"
    assert "accessToken" in response.json()["data"]

def test_register_user_missing_fields():
    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe"
    })

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("email" in error["loc"] for error in errors)
    assert any("password" in error["loc"] for error in errors)


def test_register_user_duplicate_email():
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"  # Add this line
    }

    # First registration should be successful
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Second registration with the same email should fail
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("email" in error["loc"] for error in errors)



def test_token_generation():
    response = client.post("/auth/login", json={
        "email": "john.doe@example.com",
        "password": "password123"
    })

    assert response.status_code == 201
    token = response.json()["data"]["accessToken"]

    # Decode the token without verification to check its content
    decoded_token = jwt.decode(token, options={"verify_signature": False})

    assert decoded_token["sub"] == "john.doe@example.com"  # Update this line

    # Check the token's expiration time
    assert "exp" in decoded_token
    expiration_time = datetime.fromtimestamp(decoded_token["exp"])
    assert expiration_time > datetime.now()
    assert expiration_time < datetime.now() + timedelta(minutes=30)


def test_organisation_data_access():
    # Login as a user and get their token
    response = client.post("/auth/login", json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    assert response.status_code == 201  # Update this line
    token = response.json()["data"]["accessToken"]  # Update this line

    # Try to access the user's own organisation's data
    response = client.get("/organisations/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

    # Try to access another organisation's data
    response = client.get("/organisations/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
