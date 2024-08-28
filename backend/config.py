from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_PATH = Path(__file__).parent
PROJECT_PATH = Path(__file__).parent.parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_PATH / ".env")

    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str

    REDIS_PORT: str
    REDIS_USER: str
    REDIS_HOST: str
    REDIS_PASSWORD: str


@lru_cache
def get_config() -> Config:
    return Config()
