from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import DbModel


class UserModel(DbModel):
  __tablename__ = "user"

  external_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  picture: Mapped[str] = mapped_column(String(255), nullable=True)
  provider: Mapped[str] = mapped_column(String(100), nullable=False)
  status: Mapped[str] = mapped_column(String(15), nullable=False)
