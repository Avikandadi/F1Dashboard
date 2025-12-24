"""
Core application configuration
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "F1 Dashboard API"
    api_description: str = "API for F1 race results, telemetry, and predictions"
    api_version: str = "1.0.0"
    
    # Database Configuration
    database_url: str = "sqlite:///./f1_dashboard.db"
    
    # Cache Configuration
    enable_cache: bool = True
    cache_ttl_hours: int = 24
    
    # FastF1 Configuration
    fastf1_cache_dir: str = "./fastf1_cache"
    
    # ML Model Configuration
    model_path: str = "./models"
    
    # CORS Configuration
    allowed_origins: list[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()


settings = get_settings()
