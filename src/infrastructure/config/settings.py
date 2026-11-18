from datetime import timedelta
from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from src.application.dtos.auth import TokenSettings


class Settings(BaseSettings):
  # Database
  database_host: str = "localhost"
  database_port: str = "5432"
  database_user: str = "user"
  database_password: str = "password"
  database_name: str = "mydb"
  database_echo: bool = False  # set True in development to log SQL

  # Google
  gemini_api_key: str = "xxxx"

  # OpenAI
  openai_api_key: str = "xxxxx"

  # AI
  ai_agent: str = "openai"
  ai_model: str = "gpt-4o-mini"
  ai_temperature: float = 0.0
  # Exa
  exa_api_key: str = "xxxxx"

  # Langsmith
  langsmith_api_key: str = "xxxxx"

  # App
  debug: bool = False
  app_name: str = "Study Planner"

  # RabbitMQ
  rabbitmq_prefetch_count: int = 10
  rabbitmq_url: str = "amqp://admin:pass@localhost:5672/"

  # Auth (JWT)
  jwt_secret_key: str = "change-me-jwt-secret-key-at-least-32-bytes"
  jwt_access_token_expire_minutes: int = 15
  jwt_refresh_token_expire_days: int = 7

  allowed_origins: Annotated[list[str], NoDecode] = []

  log_level: str = "INFO"

  @field_validator("allowed_origins", mode="before")
  @classmethod
  def decode_origins(cls, v: str) -> list[str]:
    return [origin.strip() for origin in v.split(",")]

  @property
  def token_settings(self) -> TokenSettings:
    return TokenSettings(
      access_token_expires_in=timedelta(minutes=self.jwt_access_token_expire_minutes),
      refresh_token_expires_in=timedelta(days=self.jwt_refresh_token_expire_days),
    )

  @property
  def database_url(self) -> str:
    return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
  return Settings()
