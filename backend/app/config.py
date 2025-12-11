from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    database_url: str
    
    telegram_bot_token: str
    telegram_webhook_url: str = ""
    
    gemini_api_key: str
    
    backend_port: int = 8000
    secret_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
