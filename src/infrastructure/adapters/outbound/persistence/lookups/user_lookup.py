from sqlalchemy import select

from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.infrastructure.adapters.outbound.persistence.mappers.user_mapper import (
  map_user_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.user_model import UserModel
from src.infrastructure.config.database import Database
from src.shared.option import Option


class UserLookupAdapter:
  def __init__(self, db: Database):
    self._db = db

  async def get_by_email(self, email: Email) -> Option[User]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(UserModel).where(UserModel.email == str(email))
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_user_model_to_domain(row))
