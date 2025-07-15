"""
Pytest configuration and fixtures for testing.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from datetime import datetime

from app.main import app
from core.db import get_db
from app.api.v1.film_routes import get_film_service
from app.api.v1.customer_routes import get_rental_service
from app.api.v1.ai_routes import get_ai_service
from core.deps import get_auth_handler

# Configure pytest to use asyncio as the default async backend
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_auth_handler():
    """Create a mock auth handler."""
    handler = AsyncMock()
    
    # Mock admin user response
    mock_admin_user = MagicMock()
    mock_admin_user.user_id = 1
    mock_admin_user.first_name = "Admin"
    mock_admin_user.last_name = "User"
    mock_admin_user.email = "admin@test.com"
    mock_admin_user.is_active = True
    
    handler.get_admin_user.return_value = mock_admin_user
    return handler


@pytest.fixture
async def async_client(mock_db_session):
    """Create async test client with mocked database."""
    def override_get_db():
        yield mock_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
async def async_film_client(mock_film_service):
    """Create async test client with mocked film service."""
    app.dependency_overrides[get_film_service] = lambda: mock_film_service
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def async_rental_client(mock_rental_service, mock_auth_handler):
    """Create async test client with mocked rental service and auth handler."""
    app.dependency_overrides[get_rental_service] = lambda: mock_rental_service
    app.dependency_overrides[get_auth_handler] = lambda: mock_auth_handler
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def async_ai_client(mock_ai_service):
    """Create async test client with mocked AI service."""
    app.dependency_overrides[get_ai_service] = lambda: mock_ai_service
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def mock_film_service():
    """Create a mock film service."""
    service = AsyncMock()
    
    # Mock get_films response
    mock_response = {
        "films": [
            {
                "film_id": 1,
                "title": "Test Action Film",
                "description": "An action test film",
                "language": "English",
                "language_id": 1,
                "rental_duration": 3,
                "rental_rate": 4.99,
                "replacement_cost": 19.99,
                "streaming_available": False,
                "last_update": datetime.utcnow().isoformat(),
                "release_year": 2020,
                "length": 120,
                "rating": "PG-13",
                "special_features": ["Trailers"],
                "categories": ["Action"]
            }
        ],
        "total": 1,
        "page": 1,
        "page_size": 10
    }
    service.get_films.return_value = mock_response
    
    return service


@pytest.fixture
def mock_rental_service():
    """Create a mock rental service."""
    service = AsyncMock()
    
    # Mock create_rental response
    mock_response = {
        "rental_id": 1,
        "customer_id": 1,
        "inventory_id": 1,
        "film_title": "Test Action Film",
        "rental_date": datetime.utcnow().isoformat(),
        "message": "Rental created successfully"
    }
    service.create_rental.return_value = mock_response
    
    return service


@pytest.fixture
def mock_ai_service():
    """Create a mock AI service."""
    service = AsyncMock()
    
    # Mock ask response
    service.ask.return_value = "This is a test AI response."
    
    # Mock film_summary response
    mock_summary_response = {
        "title": "Test Action Film",
        "summary": "This is a test film summary.",
        "rating": "PG-13",
        "recommended": True
    }
    service.film_summary.return_value = mock_summary_response
    
    return service 