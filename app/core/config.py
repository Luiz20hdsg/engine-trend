import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas de variáveis de ambiente.
    """
    DATABASE_URL: str
    HASDATA_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    class Config:
        # O .env tem prioridade sobre as variáveis de ambiente do sistema
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()