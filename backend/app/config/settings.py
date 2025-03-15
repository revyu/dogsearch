import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Поиск потерянных животных"
    VK_SERVICE_KEY: str = os.getenv("VK_SERVICE_KEY", "")
    VK_APP_ID: str = "your_app_id"  # ID вашего приложения VK
    VK_APP_SECRET: str = os.getenv("VK_APP_SECRET", "")
    VK_SECRET_KEY: str = "your_secret_key"  # Защищённый ключ вашего приложения
    
    #заглушки для настроек базы данных, которые будут добавлены позже
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    class Config:
        env_file = ".env"

settings = Settings()
