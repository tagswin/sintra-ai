"""
Configuration de Sintra AI
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration de l'application
    """
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Agent Configuration
    agent_name: str = "Sintra"
    agent_model: str = "gpt-4-turbo-preview"
    max_iterations: int = 50
    temperature: float = 0.7
    
    # Database
    database_url: str = "sqlite:///./sintra.db"
    redis_url: str = "redis://localhost:6379"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Limits
    max_task_duration: int = 3600  # secondes
    max_concurrent_tasks: int = 5
    max_memory_size: int = 1000  # nombre d'entrées
    
    # Workspace
    workspace_dir: str = "./workspace"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance globale de configuration
settings = Settings()

