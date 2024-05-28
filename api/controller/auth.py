from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from service.auth import AuthService

router = APIRouter()
security = HTTPBasic()

@router.get("/login", tags=["Authentication"], summary="Login Endpoint", description="Authenticate user with username and password.")
def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """
    Authenticate a user using HTTP Basic Authentication.

    - **username**: User's username
    - **password**: User's password
    """

    if not AuthService.authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username}