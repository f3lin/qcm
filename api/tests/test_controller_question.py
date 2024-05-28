from fastapi.testclient import TestClient
import pytest
from main import app
from models import CSVQuestion
from service.question import delete_question

client = TestClient(app)

# Fixtures for authentication
@pytest.fixture
def user_credentials():
    return {
        "username": "alice",
        "password": "wonderland"
    }

@pytest.fixture
def admin_credentials():
    return {
        "username": "admin",
        "password": "4dm1N"
    }

def test_get_questions(user_credentials):
    response = client.get("/api-v1/questions/?use=Test%20de%20positionnement&subjects=BDD&subjects=Docker&num_questions=5",
                           auth=(user_credentials['username'], user_credentials['password']))
    assert response.status_code == 200
    assert len(response.json()) == 5  # Assuming there are at least 5 questions available

def test_add_question(admin_credentials):
    question = [CSVQuestion(
        question = "What is the capital of France?",
        subject = "Geography",
        use= "Quiz",
        correct = "Paris",
        responseA = "A1",
        responseB = "A2",
        responseC = "A3",
        responseD = "A4",
        remark = ""
    )]
    question_data = [q.model_dump() for q in question]

    response = client.post("/api-v1/questions/", 
                        auth=(admin_credentials['username'], admin_credentials['password']),
                        json=question_data[0])
    assert response.status_code == 200
    assert response.json() == question_data[0]
    delete_question(question[0])

def test_get_unique_subjects():
    response = client.get("/api-v1/questions/subjects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_unique_uses():
    response = client.get("/api-v1/questions/uses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)