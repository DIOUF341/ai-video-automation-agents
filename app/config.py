from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VideoAgent Studio"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    output_dir: str = "output"
    openai_api_key: str = ""
    tts_provider: str = "gtts"
    default_language: str = "fr"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
