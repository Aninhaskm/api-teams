"""
Arquivo principal de configuração do projeto.
Define a classe Settings para carregar variáveis de ambiente e configurações da API Teams.
"""
from pydantic_settings import BaseSettings 
from functools import lru_cache # Fornece funções de ordem superior e decoradores, caching inteligente

class Settings(BaseSettings):
    APP_NAME: str = "Teams messenger API"
    CLIENT_ID: str
    CLIENT_SECRET: str
    TENANT_ID: str
    SCOPE: str
    AUTHORITY: str
    GRAPH_API_ENDPOINT: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
