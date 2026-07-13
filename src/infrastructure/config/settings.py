from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
  # Database
  database_host: str = "localhost"
  database_port: str = "5432"
  database_user: str = "user"
  database_password: str = "password"
  database_name: str = "mydb"
  database_echo: bool = False  # set True in development to log SQL

  # Google
  google_api_key: str = "xxxx"
  google_agent_model: str = "xxxx"

  # Exa
  exa_api_key: str = "xxxxx"

  # Langsmith
  langsmith_api_key: str = "xxxxx"

  # App
  debug: bool = False
  app_name: str = "Study Planner"

  rabbitmq_prefetch_count: int = 10
  rabbitmq_url: str = "amqp://admin:pass@localhost:5672/"

  allowed_origins: Annotated[list[str], NoDecode] = []

  @field_validator("allowed_origins", mode="before")
  @classmethod
  def decode_origins(cls, v: str) -> list[str]:
    return [origin.strip() for origin in v.split(",")]

  @property
  def database_url(self) -> str:
    return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
  return Settings()
