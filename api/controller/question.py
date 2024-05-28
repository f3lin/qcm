from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from service.question import find_questions, create_question, get_subjects, get_uses
from models import CSVQuestion
from service.auth import AuthService

router = APIRouter()
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticates a regular user based on provided credentials.

    Args:
        credentials (HTTPBasicCredentials): The HTTP basic authentication credentials.

    Raises:
        HTTPException: If the provided credentials are invalid.

    Returns:
        str: The username if authentication is successful.
    """
    if not AuthService.authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username

def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticates an admin user based on provided credentials.

    Args:
        credentials (HTTPBasicCredentials): The HTTP basic authentication credentials.

    Raises:
        HTTPException: If the provided credentials are invalid or if the user is not an admin.

    Returns:
        str: The username if authentication is successful.
    """
    if not AuthService.is_admin(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return credentials.username


@router.get("/", response_model=List[CSVQuestion], tags=['Questions, Authentication'])
def get_questions(
        use: str, 
        subjects: List[str] = Query(...), 
        num_questions: int = Query(5, gt=0, le=20), 
        username: str = Depends(authenticate_user)
    ):
    """
    Fetches questions based on the specified criteria.

    Args:
        use (str): Use of the questions (e.g., "Exam", "Quiz").
        subjects [str]: list of subjects.
        num_questions (int): Number of questions to fetch.
        username (str): The username of the authenticated user.

    Returns:
        List[CSVQuestion]: A list of CSVQuestion objects representing the questions.

    Raises:
        HTTPException: If there is an error in fetching the questions.
    """
    try:
        questions = find_questions(use, subjects, num_questions)
        return questions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=CSVQuestion, tags=["Questions, Authentication"])
def add_question(
        question: CSVQuestion,
        username: str = Depends(authenticate_admin)
    ):
    """
    Adds a new question.

    Args:
        question (CSVQuestion): The new question to add.
        username (str): The username of the authenticated admin user.

    Returns:
        CSVQuestion: The added question.

    Raises:
        HTTPException: If there is an error in adding the question.
    """
    try:
        create_question(question)
        return question
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/subjects/", response_model=List[str], tags=["Questions"])
def get_unique_subjects():
    """
    Fetches unique subjects.

    Returns:
        List[str]: A list of unique subjects.
    """
    return get_subjects()

@router.get("/uses/", response_model=List[str], tags=["Questions"])
def get_unique_uses():
    """
    Fetches unique uses.

    Returns:
        List[str]: A list of unique uses.
    """
    return get_uses()
