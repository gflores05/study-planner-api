from datetime import datetime

from sqlalchemy import DateTime, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import DbModel


class UserModel(DbModel):
  __tablename__ = "user"

  email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
  status: Mapped[str] = mapped_column(String(15), nullable=False)
  last_login_on: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), nullable=True
  )
