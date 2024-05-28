import os.path
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from csv_management import load_csv
from controller import auth, question

csv_url = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"
path = 'data/data.csv'

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager to load CSV data into the application during startup.

    Parameters:
    - app (FastAPI): The FastAPI application instance.

    Yields:
    - None

    Usage:
    async with lifespan(app):
        # Load CSV data into the application
    """
    load_csv(csv_url, path)
    load_csv(csv_url, f"tests/{path}")
    yield

app = FastAPI(
                lifespan=lifespan,
                openapi_tags=[
                    {
                        'name': 'Questions',
                        'description': 'Operations related to questions in the QCM'
                    },
                    {
                        'name': 'Health',
                        'description': 'health check operations'
                    },
                    {
                        'name': 'Authentication',
                        'description': 'Authentication and health check operations'
                    }
                ]
            )

prefix = "/api-v1"

@app.get(f"{prefix}/healthcheck/", tags=["Health"], summary="Health Check Endpoint", description="Check the health status of the API.")
async def health_check():
    """
    Check the health status of the API.

    Returns:
    - dict: A dictionary indicating the status of the API. If the data file exists, returns {"status": "ok"}; otherwise, raises a 503 error.

    Raises:
    - HTTPException: If the data file is not available, raises a 503 error with the message "Service Unavailable".
    """
    if os.path.isfile(path):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=503, detail="Service Unavailable")

app.include_router(auth.router, prefix=f"{prefix}/auth")
app.include_router(question.router, prefix=f"{prefix}/questions")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)