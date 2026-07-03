import uuid
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import DateTime, Integer, Uuid, func
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from sqlalchemy.orm import (
  DeclarativeBase,
  Mapped,
  declared_attr,
  mapped_column,
)


class DbModel(DeclarativeBase):
  @declared_attr
  def id(self) -> Mapped[uuid.UUID]:
    return mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

  @declared_attr
  def created_on(self) -> Mapped[datetime]:
    return mapped_column(
      DateTime(timezone=True), server_default=func.now(), nullable=False
    )

  @declared_attr
  def modified_on(self) -> Mapped[datetime]:
    return mapped_column(
      DateTime(timezone=True), server_default=func.now(), nullable=False
    )

  @declared_attr
  def version(self) -> Mapped[int]:
    return mapped_column(Integer, nullable=False)


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
  global _engine
  if _engine is None:
    from src.infrastructure.config.settings import get_settings

    settings = get_settings()

    _engine = create_async_engine(
      settings.database_url,
      echo=settings.db_echo,  # logs SQL — useful in development
      pool_size=10,
      max_overflow=20,
      pool_pre_ping=True,  # drops stale connections automatically
    )
  return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
  global _session_factory
  if _session_factory is None:
    _session_factory = async_sessionmaker(
      bind=get_engine(),
      class_=AsyncSession,
      expire_on_commit=False,  # avoids lazy-load errors after commit
      autocommit=False,
      autoflush=False,
    )
  return _session_factory


# ---------------------------------------------------
# FastAPI dependency — one session per request
# ---------------------------------------------------


async def get_session() -> AsyncGenerator[AsyncSession, None]:
  factory = get_session_factory()
  async with factory() as session:
    try:
      yield session
      await session.commit()
    except Exception:
      await session.rollback()
      raise
    finally:
      await session.close()


# ---------------------------------------------------
# Startup / shutdown — called from main.py
# ---------------------------------------------------


async def init_db() -> None:
  """Seed datatabase if it's necessary"""
  pass


async def close_db() -> None:
  """Dispose the engine cleanly on shutdown."""
  global _engine, _session_factory
  if _engine:
    await _engine.dispose()
    _engine = None
    _session_factory = None
