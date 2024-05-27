import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from typing import List

from main import app, Question

@pytest.mark.asyncio
async def test_read_qcm():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/qcm/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(isinstance(item, dict) for item in response.json())

@pytest.mark.asyncio
async def test_read_qcm_question_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First ensure we have at least one item
        qcm_response = await ac.get("/qcm/")
        qcm = qcm_response.json()
        if qcm:
            first_id = qcm[0]['id']
            response = await ac.get(f"/qcm/{first_id}")
            assert response.status_code == 200
            assert response.json()['id'] == first_id

@pytest.mark.asyncio
async def test_read_qcm_question_by_id_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/qcm/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}

