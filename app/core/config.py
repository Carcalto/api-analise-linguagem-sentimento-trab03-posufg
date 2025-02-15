import os
from pydantic import BaseSettings
from functools import lru_cache

# Define as configurações da aplicação utilizando Pydantic BaseSettings
class Settings(BaseSettings):
    API_KEY: str = os.getenv("API_KEY", "default_key") # API Key para autenticação, default 'default_key' se não definida no env
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO") # Nível de logging da aplicação, default 'INFO' se não definido no env
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development") # Ambiente da aplicação, default 'development' se não definido no env

    class Config:
        env_file = ".env" # Especifica o arquivo .env para carregar variáveis de ambiente

# Função para obter as configurações da aplicação com cache para otimização
@lru_cache()
def get_settings():
    return Settings() # Retorna uma instância de Settings com as configurações carregadas
