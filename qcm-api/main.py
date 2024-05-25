import csv
import asyncio
import httpx
from typing import List
from fastapi import FastAPI, HTTPException
from io import StringIO
from contextlib import asynccontextmanager
from pydantic import BaseModel

from pydantic import BaseModel

class Question(BaseModel):
    id: int
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str
    remark: str


# URL to your CSV file
csv_url = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"

# Asynchronous function to fetch CSV from URL with retry
async def fetch_csv_from_url_with_retry(url, max_attempts=3, retry_delay=1):
    for attempt in range(max_attempts):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    csv_questions = response.text
                    csv_reader = csv.DictReader(StringIO(csv_questions))
                    return list(csv_reader)
                else:
                    raise HTTPException(status_code=500, detail="Failed to fetch CSV from URL")
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                await asyncio.sleep(retry_delay)
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch CSV from URL after multiple attempts")

# Initialize questions variable
qcm: List[Question] = []

# Have a look on https://fastapi.tiangolo.com/advanced/events/
# Asynchronous startup event to fetch CSV questions
@asynccontextmanager
async def lifespan(app: FastAPI):
    global qcm
    csv_data  = await fetch_csv_from_url_with_retry(csv_url)

    # Add an "id" column to the CSV questions
    for i, row in enumerate(csv_data ):
        question_data = {'id': i}
        question_data.update(row)
        qcm.append(Question(**question_data))
    
    yield

    # Clean up the CSV questions and release the resources
    qcm.clear()

app = FastAPI(
                lifespan=lifespan,
                openapi_tags=[
                    {
                        'name': 'Questions',
                        'description': 'default functions that are used to deal with QCM'
                    },
                    {
                        'name': 'Uses',
                        'description': 'functions that are used to deal with Uses'
                    },
                    {
                        'name': 'Subjects',
                        'description': 'functions that are used to deal with Subjects'
                    }
                ]
            )

# Function to get all items
def get_qcm():
    return qcm

# Function to get an item by its ID
def get_qcm_question_by_id(question_id: int):
    for question in qcm:
        if question.id == question_id:
            return question
    raise HTTPException(status_code=404, detail="Question not found")

# Endpoint to get all qcm questions
@app.get("/qcm/", response_model=List[Question], tags=['Questions'], summary="Retrieve all questions", description="Get a list of all questions in the QCM.")
async def read_qcm():
    return get_qcm()

# Endpoint to get an qcm question by its ID
@app.get("/qcm/{question_id}", response_model=Question, tags=['Questions'], summary="Retrieve a question by ID", description="Get the details of a specific question by its ID.")
async def read_qcm_question_by_id(question_id: int):
    return get_qcm_question_by_id(question_id)
