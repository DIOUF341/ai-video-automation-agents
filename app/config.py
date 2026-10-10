"""Configuration de l'application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "VideoAgent Studio"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    replicate_api_key: str = ""
    debug: bool = False
    output_dir: str = "output"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
