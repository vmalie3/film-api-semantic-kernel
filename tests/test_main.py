"""
Test main application startup.
"""

import pytest
from app.main import app


@pytest.mark.anyio
async def test_app_startup():
    """Test that the FastAPI app starts correctly."""
    assert app is not None
    assert app.title == "Mini Pagilla API" 