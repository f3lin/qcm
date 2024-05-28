from pydantic import BaseModel
from typing import Optional

class CSVQuestion(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = ""
    remark: Optional[str] = ""

class User(BaseModel):
    id: int
    name: str
    password: str