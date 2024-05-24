import csv
import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from io import StringIO

app = FastAPI()

# URL to your CSV file
csv_url = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"

# Asynchronous function to fetch CSV from URL with retry
async def fetch_csv_from_url_with_retry(url, max_attempts=3, retry_delay=1):
    for attempt in range(max_attempts):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    csv_data = response.text
                    csv_reader = csv.DictReader(StringIO(csv_data))
                    return list(csv_reader)
                else:
                    raise HTTPException(status_code=500, detail="Failed to fetch CSV from URL")
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                await asyncio.sleep(retry_delay)
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch CSV from URL after multiple attempts")

# Asynchronously fetch CSV data with retry
async def get_csv_data():
    return await fetch_csv_from_url_with_retry(csv_url)

# Get CSV data synchronously with retry
data = asyncio.run(get_csv_data())

# Add an "id" column to the CSV data
for i, row in enumerate(data):
    row['id'] = i

# Function to get all items
def get_items():
    return data

# Function to get an item by its ID
def get_item(item_id: int):
    for item in data:
        if item['id'] == str(item_id):
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to get all items
@app.get("/items/")
async def read_items():
    return get_items()

# Endpoint to get an item by its ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return get_item(item_id)
