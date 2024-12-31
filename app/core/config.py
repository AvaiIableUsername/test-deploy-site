from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pydantic import BaseModel


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class Settings(BaseSettings):
    database_url: PostgresDsn = (
        "postgresql+asyncpg://postgres:111@localhost:5432/e-commerce"
    )
    app_config: AppConfig = AppConfig()
    model_config = SettingsConfigDict(env_file="./env")


settings = Settings()
