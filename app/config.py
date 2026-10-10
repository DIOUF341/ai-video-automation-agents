"""Configuration de l'application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Paramètres globaux de l'application."""
    app_name: str = "VideoAgent Studio"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
