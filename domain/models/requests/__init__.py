"""
Request schemas for API input validation.
"""

from .film import CreateFilmRequest, UpdateFilmRequest, FilmSummaryRequest
from .rental import CreateRentalRequest

__all__ = [
    # Film requests
    "CreateFilmRequest",
    "UpdateFilmRequest",
    # Rental requests
    "CreateRentalRequest",
    "FilmSummaryRequest",
] 