import os
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/api-v1/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_invalid_path_health_check():
    # Temporarily rename the data file to simulate unavailability
    os.rename("data/data.csv", "data/data_temp.csv")
    response = client.get("/api-v1/healthcheck/")
    assert response.status_code == 503
    assert response.json() == {"detail": "Service Unavailable"}
    # Rename the file back to its original name
    os.rename("data/data_temp.csv", "data/data.csv")
