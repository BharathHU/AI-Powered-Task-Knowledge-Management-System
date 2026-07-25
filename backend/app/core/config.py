from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "mysql+pymysql://task_user:task_password@localhost:3306/task_knowledge"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 120
    admin_email: str = "admin@example.com"
    admin_password: str = "admin123"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    upload_dir: str = "storage/uploads"
    index_dir: str = "storage/index"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
