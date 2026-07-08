import uuid
from contextlib import asynccontextmanager
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


class Database:
  _engine: AsyncEngine | None = None
  _session_factory: async_sessionmaker[AsyncSession] | None = None

  def __init__(self, database_url: str, db_echo: bool) -> None:
    self.database_url = database_url
    self.db_echo = db_echo

  @asynccontextmanager
  async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    factory = self._get_session_factory()
    async with factory() as session:
      try:
        yield session
        await session.commit()
      except Exception:
        await session.rollback()
        raise
      finally:
        await session.close()

  def _get_session_factory(self) -> async_sessionmaker[AsyncSession]:
    if self._session_factory is None:
      self._session_factory = async_sessionmaker(
        bind=self._get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,  # avoids lazy-load errors after commit
        autocommit=False,
        autoflush=False,
      )
    return self._session_factory

  def _get_engine(self) -> AsyncEngine:
    if self._engine is None:
      self._engine = create_async_engine(
        self.database_url,
        echo=self.db_echo,  # logs SQL — useful in development
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # drops stale connections automatically
      )
    return self._engine

  # ---------------------------------------------------
  # Startup / shutdown — called from main.py
  # ---------------------------------------------------

  async def init(self) -> None:
    """Create all tables on startup (use Alembic in production instead)."""
    async with self._get_engine().begin() as conn:
      await conn.run_sync(DbModel.metadata.create_all)

  async def close(self) -> None:
    """Dispose the engine cleanly on shutdown."""
    if self._engine:
      await self._engine.dispose()
      self._engine = None
      self._session_factory = None
