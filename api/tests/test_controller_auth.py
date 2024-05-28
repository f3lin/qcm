from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.get(
        "/api-v1/auth/login",
        auth=("alice", "wonderland")
    )
    assert response.status_code == 200
    assert response.json() == {"username": "alice"}

def test_login_invalid_username():
    response = client.get(
        "/api-v1/auth/login",
        auth=("invaliduser", "wonderland")
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_invalid_password():
    response = client.get(
        "/api-v1/auth/login",
        auth=("alice", "invalidpassword")
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_no_credentials():
    response = client.get("/api-v1/auth/login")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == 'Basic'
