import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn

    model_config = SettingsConfigDict(env_file=os.path.dirname(os.getcwd()) + '/.env')


settings = Settings()