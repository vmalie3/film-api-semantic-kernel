"""
AI Kernel setup and plugin management.
"""
import time
from contextlib import asynccontextmanager
from semantic_kernel import Kernel
from domain.ai_kernel.plugins.FilmPlugin import FilmPlugin
from domain.services.film_service import FilmService
from domain.repositories.film_repository import FilmRepository
from core.db import get_engine_and_session_factory
from core.logging import get_logger
from core.config import settings
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

logger = get_logger(__name__)

@asynccontextmanager
async def kernel_lifespan():
    start_time = time.time()
    logger.info("Initializing AI kernel")
    
    try:
        kernel = Kernel()
        await configure_kernel(kernel)
        
        init_duration = time.time() - start_time
        logger.info("AI kernel initialization completed", duration_ms=round(init_duration * 1000, 2))
        
        yield kernel
        
    except Exception as e:
        logger.error("Failed to initialize AI kernel", error=str(e), exc_info=True)
        raise
    finally:
        logger.info("Shutting down AI kernel services")
        cleanup_duration = time.time() - start_time
        logger.info("AI kernel cleanup completed", duration_ms=round(cleanup_duration * 1000, 2))

async def configure_kernel(kernel: Kernel):
    await add_services(kernel)
    await add_plugins_and_functions(kernel)

async def add_plugins_and_functions(kernel: Kernel):  
    # Get the engine and session factory
    _, session_factory = get_engine_and_session_factory("film")
    
    # Create a session with proper lifecycle management
    async with session_factory() as session:
        film_repository = FilmRepository(session)
        film_service = FilmService(film_repository)
        film_plugin = FilmPlugin(film_service)
        kernel.add_plugin(film_plugin, plugin_name="FilmPlugin")

async def add_services(kernel: Kernel):
    if settings.azure_openai_api_key and settings.azure_openai_endpoint:
        # Use Azure OpenAI
        logger.info("Initializing Azure OpenAI service", endpoint=settings.azure_openai_endpoint)
        azure_chat_service = AzureChatCompletion(
            api_key=settings.azure_openai_api_key,
            endpoint=settings.azure_openai_endpoint,
            deployment_name=settings.azure_openai_deployment_name,
            api_version=settings.azure_openai_api_version,
            service_id=settings.azure_openai_service_id
        )
        kernel.add_service(azure_chat_service)
        logger.info("Azure OpenAI service initialized successfully")
    else:
        logger.warning("Azure OpenAI configuration not found, AI features will be disabled")
