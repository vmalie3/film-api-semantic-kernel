# Mini Pagilla API

A well-structured FastAPI application framework ready for development.

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run the application:
   ```bash
   poetry run python -m app.main
   ```

3. The API will be available at: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs
   - Root endpoint: http://127.0.0.1:8000/api/v1/
   - Health check: http://127.0.0.1:8000/api/v1/health

## Example CURL commands

** All endpoints can be tested via http://127.0.0.1:8000/docs **

### Films API

**Get films with pagination:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/films/?page=1&page_size=10" \
  -H "accept: application/json"
```

**Get films with category filter:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/films/?category=Action" \
  -H "accept: application/json"
```

### Customer Rentals API

**Create a rental (requires admin authentication):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/customers/1/rentals" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "inventory_id": 1,
    "staff_id": 1
  }'
```

### AI Chat API

**Ask a question:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/ai/ask?question=What%20is%20the%20weather%20like%20today?" \
  -H "accept: application/json"
```

**Generate film summary:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ai/summary" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "film_id": 1
  }'
```

## Setup Local DB

### Clone Repository

```bash
git clone https://github.com/devrimgunduz/pagila.git
```

**follow README instructions**

### Setup Existing DB Entities

Example in `domain/entities`

## Migrations (initial)

### Initialize Alembic

```Bash
alembic init alembic
```

### Set Base (for existing tables / setup)

add correct path in env.py within alembic folder

```Python
from domain.entities import Base  # This imports all models through __init__.py
from domain.entities import *  # This ensures all models are imported

# add your model's MetaData object here
target_metadata = Base.metadata
```

then run command:

```Bash
alembic -n Film stamp head
```

### Run Migrations

Make desired changes to your schema then run:

```Bash
alembic -n Film revision --autogenerate -m "Add new field XYZ"
```

**review the generated file in `alembic/versions` to ensure it's only tracking desired change**

make any needed changes (you may delete non committed version file if needed) then run:

```Bash
alembic -n Film upgrade head
```


## Development

### Running Tests

The project includes focused test coverage using pytest with mocked dependencies for fast, reliable testing.

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api_endpoints.py -v

# Run specific test
python -m pytest tests/test_api_endpoints.py::test_get_films_happy_path -v

# Run tests with output (useful for debugging)
python -m pytest tests/ -v -s

# Run tests with coverage report
python -m pytest tests/ --cov=app --cov-report=html

# Run tests in parallel (if you have pytest-xdist installed)
python -m pytest tests/ -n auto
```

### Test Coverage

**Run Tests**
```Bash
poetry run pytest tests/ -v --asyncio-mode=auto
```

The test suite includes focused happy path tests for core API endpoints:

**API Endpoint Tests:**
- `test_get_films_happy_path`: GET /api/v1/films/ with pagination
- `test_create_rental_happy_path`: POST /api/v1/customers/{id}/rentals with authentication
- `test_ask_happy_path`: GET /api/v1/ai/ask for AI chat functionality
- `test_summary_happy_path`: POST /api/v1/ai/summary for film summary generation

**Test Architecture:**
- **Mocked Dependencies**: Uses FastAPI's dependency override system to inject mock services
- **Endpoint-Specific Clients**: Separate test clients for each service (film_client, rental_client, ai_client)
- **Structured Mock Data**: Mock responses that match actual API response models
- **Fast Execution**: No database setup required, tests run in milliseconds
- **Reliable**: Tests are isolated and don't depend on external services

**Test Features:**
- FastAPI dependency injection testing
- Response model validation
- Authentication testing (Bearer token)
- Mock service integration
- Clean test isolation

### Configuration
- Application settings are managed in `core/config.py`
- Environment variables can be set in `.env` file
- Database configuration is in `core/db.py`

### Adding New Features
- **API Routes**: Add to `app/api/v1/` directory (e.g., films.py, customers.py)
- **Request/Response Models**: Add Pydantic schemas in `domain/models/requests/` and `domain/models/responses/`
- **Database Models**: Add SQLAlchemy models in `domain/entities/`
- **Business Logic**: Add services in `domain/services/`
- **AI/ML Features**: Add to `domain/ai_kernel/` (plugins, functions, etc.)
- **Utilities**: Add utility functions in `domain/utils/`
- **Tests**: Add tests in `tests/` directory

## Architecture

This project follows a **Domain-Driven Design (DDD)** architecture with clear separation of concerns:

### Core Layer (`core/`)
Contains infrastructure and cross-cutting concerns:
- **Configuration**: Application settings and environment variables
- **Database**: Database connection and session management
- **Security**: Authentication and authorization utilities
- **Middleware**: Request/response processing middleware

### Domain Layer (`domain/`)
Contains the business logic and domain models:
- **Entities**: Database models representing business entities
- **Services**: Business logic and use cases
- **Models**: Request/response schemas for API contracts
- **Utils**: Domain-specific utility functions
- **AI Kernel**: Semantic Kernel integration for AI capabilities
- **Repositories**: Data access patterns (future expansion)

### Application Layer (`app/`)
Contains the application entry points and API interfaces:
- **Main**: Application startup and configuration
- **API**: REST endpoints and route handlers

### Benefits of this Architecture:
- **Separation of Concerns**: Clear boundaries between layers
- **Testability**: Easy to unit test business logic
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features and extend functionality
- **AI Integration**: Semantic Kernel naturally fits in the domain layer

## Next Steps

This project structure provides:
- ✅ **Domain-Driven Design** architecture with clear separation of concerns
- ✅ **FastAPI** application with organized structure
- ✅ **Configuration management** with environment variables (Poetry + pip support)
- ✅ **Database setup** with SQLAlchemy and Alembic migrations
- ✅ **AI/ML Integration** with Semantic Kernel
- ✅ **API versioning** support with RESTful endpoints
- ✅ **Comprehensive test framework** with pytest-asyncio
- ✅ **In-memory test database** with SQLite
- ✅ **Authentication and authorization** testing
- ✅ **Business logic services** (Film, Rental, AI Chat)
- ✅ **AI-powered features** (Film summaries, chat capabilities)
- ✅ **Model converters** and utilities
- ✅ **Development tools** (formatting, linting)

You can now start building your API by:
1. **Adding new entities** in `domain/entities/`
2. **Creating business services** in `domain/services/`
3. **Building API endpoints** in `app/api/v1/`
4. **Extending AI capabilities** in `domain/ai_kernel/`
5. **Adding comprehensive tests** in `tests/` 
6. **Adding and using agents**