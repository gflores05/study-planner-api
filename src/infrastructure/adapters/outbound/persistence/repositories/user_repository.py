from sqlalchemy import select

from src.domain.user.user import User
from src.domain.user.value_objects.user_id import UserId
from src.infrastructure.adapters.outbound.persistence.mappers.user_mapper import (
  map_user_domain_to_model,
  map_user_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.user_model import (
  UserModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class UserRepository:
  def __init__(self, db: Database):
    self._db = db

  async def get(self, id: UserId, load_children: bool = True) -> Option[User]:
    async with self._db.get_session() as session:
      result = await session.execute(select(UserModel).where(UserModel.id == str(id)))

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_user_model_to_domain(row))

  async def save(self, user: User):
    async with self._db.get_session() as session:
      user.increment_version()
      model = map_user_domain_to_model(user)
      await session.merge(model)
      await session.flush()
