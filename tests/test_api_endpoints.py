"""
API endpoint tests - one happy path test per endpoint.
"""

import pytest
from fastapi import status


@pytest.mark.anyio
async def test_get_films_async(async_film_client):
    """Async version of films test using AsyncClient."""
    url = "/api/v1/films/"
    params = {"page": 1, "page_size": 10}
    response = await async_film_client.get(url, params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "films" in data
    assert "total" in data
    assert isinstance(data["films"], list)
    assert isinstance(data["total"], int)
    assert data["total"] >= 0
    if data["films"]:
        film = data["films"][0]
        assert "film_id" in film
        assert "title" in film
        assert "description" in film
        assert "language_name" in film
        assert "language_id" in film
        assert "rental_duration" in film
        assert "last_update" in film


@pytest.mark.anyio
async def test_create_rental_async(async_rental_client):
    """Async version of rental test using AsyncClient."""
    url = "/api/v1/customers/1/rentals"
    # Use a mock token for testing - this should be handled by the mock service
    headers = {"Authorization": "Bearer mock_token_for_testing"}
    rental_data = {"inventory_id": 1, "staff_id": 1}
    response = await async_rental_client.post(url, json=rental_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "rental_id" in data
    assert "customer_id" in data
    assert "inventory_id" in data
    assert "rental_date" in data
    assert "message" in data
    assert data["customer_id"] == 1
    assert data["inventory_id"] == 1
    assert "successfully" in data["message"]


@pytest.mark.anyio
async def test_ask_async(async_ai_client):
    """Async version of AI ask test using AsyncClient."""
    url = "/api/v1/ai/ask"
    params = {"question": "What is the weather like today?"}
    response = await async_ai_client.get(url, params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.text
    assert isinstance(data, str)
    assert len(data) > 0


@pytest.mark.anyio
async def test_summary_async(async_ai_client):
    """Async version of AI summary test using AsyncClient."""
    url = "/api/v1/ai/summary"
    summary_request = {"film_id": 1}
    response = await async_ai_client.post(url, json=summary_request)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "title" in data
    assert "summary" in data
    assert "rating" in data
    assert "recommended" in data
    assert isinstance(data["summary"], str)
    assert isinstance(data["rating"], str)
    assert isinstance(data["recommended"], bool)
    assert len(data["summary"]) > 0 