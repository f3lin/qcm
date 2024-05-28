import secrets
from passlib.context import CryptContext
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simulate a user database with hashed passwords
users_db = [
    User(id=0, name="admin", password=pwd_context.hash("4dm1N")),
    User(id=1, name="alice", password=pwd_context.hash("wonderland")),
    User(id=2, name="bob", password=pwd_context.hash("builder")),
    User(id=3, name="clementine", password=pwd_context.hash("mandarine")),
]

def get_user_by_name(name: str) -> User:
    return next((user for user in users_db if user.name == name), None)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class AuthService:
    # It is best paractice to use secrets module 
    # See https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#timing-attacks
    @staticmethod
    def authenticate_user(username: str, password: str) -> bool:
        user = get_user_by_name(username)
        if user:
            is_correct_username = secrets.compare_digest(username, user.name)
            is_correct_password = verify_password(password, user.password)
            return is_correct_username and is_correct_password
        return False

    @staticmethod
    def is_admin(username: str, password: str) -> bool:
        is_correct_admin_username = secrets.compare_digest(username, get_user_by_name('admin').name)
        is_correct_admin_password = verify_password(password, get_user_by_name('admin').password)
        return is_correct_admin_username and is_correct_admin_password
