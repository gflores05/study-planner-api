import uuid
from datetime import datetime

from sqlalchemy import Integer, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class DbModel(DeclarativeBase):
  @declared_attr
  def id(self) -> Mapped[uuid.UUID]:
    return mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

  @declared_attr
  def created_on(self) -> Mapped[datetime]:
    return mapped_column(server_default=func.now(), nullable=False)

  @declared_attr
  def modified_on(self) -> Mapped[datetime]:
    return mapped_column(server_default=func.now(), nullable=False)

  @declared_attr
  def version(self) -> Mapped[datetime]:
    return mapped_column(Integer, nullable=False)
