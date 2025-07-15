from fastapi import Depends, Request
from semantic_kernel import Kernel
from domain.services.ai_chat_service import AIService
from domain.services.customer_service import CustomerService
from domain.repositories.deps import get_customer_repository
from domain.repositories.customer_repository import CustomerRepository
from domain.services.film_service import FilmService
from domain.repositories.film_repository import FilmRepository
from domain.repositories.deps import get_film_repository
from domain.services.rental_service import RentalService
from domain.repositories.rental_repository import RentalRepository
from domain.repositories.deps import get_rental_repository
from domain.services.auth_service import AuthService

def get_kernel(request: Request) -> Kernel:
    return request.app.state.kernel

def get_ai_service(kernel: Kernel = Depends(get_kernel)) -> AIService:
    return AIService(kernel)

def get_customer_service(customer_repository: CustomerRepository = Depends(get_customer_repository)):
    """Dependency to get CustomerService instance."""
    return CustomerService(customer_repository)

def get_film_service(film_repository: FilmRepository = Depends(get_film_repository)):
    """Dependency to get FilmService instance."""
    return FilmService(film_repository)

def get_rental_service(rental_repository: RentalRepository = Depends(get_rental_repository), customer_repository: CustomerRepository = Depends(get_customer_repository)):
    """Dependency to get RentalService instance."""
    return RentalService(rental_repository, customer_repository)

def get_auth_service(customer_repository: CustomerRepository = Depends(get_customer_repository)):
    """Dependency to get AuthService instance."""
    return AuthService(customer_repository)