# File: core/config.py
# Central configuration module that reads environment variables (or a .env file)
# and exposes a singleton Settings object. Every other module imports
# `settings` from here to access database URLs, JWT params, file paths, etc.

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# Application-wide settings loaded from environment variables with sensible
# defaults for local development. Used by all layers — database, security,
# storage, AI model configuration.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "mysql+pymysql://root:Bharath%402004@localhost:3306/task_knowledge_db"

    # JWT authentication
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 120

    # Default admin credentials (used during bootstrap seeding)
    admin_email: str = "admin@gmail.com.com"
    admin_password: str = "admin123"

    # CORS — allowed origins for the frontend dev server
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    # File storage paths
    upload_dir: str = "storage/uploads"
    index_dir: str = "storage/index"

    # AI / Vector search
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"


# LRU-cached factory so the Settings object is parsed only once at import time.
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
