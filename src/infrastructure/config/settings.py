from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  # Database
  database_url: str = "postgresql+asyncpg://user:password@localhost:5432/mydb"
  db_echo: bool = False  # set True in development to log SQL

  # Google
  google_api_key: str = "xxxx"
  google_agent_model: str = "xxxx"

  # Exa
  exa_api_key: str = "xxxxx"

  # Langsmith
  langsmith_api_key = "xxxxx"

  # App
  debug: bool = False
  app_name: str = "Study Planner"

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache  # singleton — reads .env once
def get_settings() -> Settings:
  return Settings()
