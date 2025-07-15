import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

env = os.getenv("ENV", "development")
file_map = {
    "development": ".env",
    "uat": ".env.uat",
    "production": ".env.production",
}
env_file_path=file_map.get(env, ".env")

class Settings(BaseSettings):  
    # App settings
    app_name: str = "Mini Pagilla API"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    environment: str = env
    
    # Database settings
    db_key: Optional[str] = None
    film_database_url: Optional[str] = None
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Global LLM service selection
    global_llm_service: str = "AzureOpenAI"  # Options: "AzureOpenAI", "OpenAI", etc.
    
    # Azure OpenAI settings
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-01"
    azure_openai_deployment_name: Optional[str] = None
    azure_openai_chat_deployment_name: Optional[str] = None
    azure_openai_text_deployment_name: Optional[str] = None
    azure_openai_embedding_deployment_name: Optional[str] = None
    azure_openai_service_id: Optional[str] = None
    
    # Security settings
    secret_key: str = Field(default="dev-secret-key")
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Redis settings (if using caching)
    redis_url: Optional[str] = None
    redis_db: int = 0

    # Auth
    jwt_secret: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 1
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    admin_token: Optional[str] = None
    class Config:
        env_file = env_file_path
        env_file_encoding = "utf-8"
        case_sensitive = False  # Allows both DATABASE_URL and database_url
        extra = "ignore"  # Ignore extra fields instead of raising validation errors


settings = Settings() 