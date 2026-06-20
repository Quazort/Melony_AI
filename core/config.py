from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    AI_KEY: str
    AI_MODEL: str
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str
    LLM_MODEL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding='utf-8')


settings = Settings()
