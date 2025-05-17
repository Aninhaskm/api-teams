from pydantic import BaseSettings 
from functools import lru_cache # Fornece funções de ordem superior e decoradores, caching inteligente

class Settings(BaseSettings):
    APP_NAME: str = "Teams messenger API"
    CLIENT_ID: str
    CLIENT_SECRET: str
    TENANT_ID: str
    SCOPE: str
    AUTHORITY: str

class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

@lru_cache() # Least Recently Used, guarda em memória o resultado da função na primeira vez que ela for chamada. 
def get_settings() -> Settings:
    return Settings()

