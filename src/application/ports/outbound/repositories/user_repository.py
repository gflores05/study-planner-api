from typing import Protocol

from src.domain.user.user import User
from src.domain.user.value_objects.user_id import UserId
from src.shared.option import Option


class UserRepository(Protocol):
  async def get(self, id: UserId, load_children: bool = True) -> Option[User]: ...
  async def save(self, user: User) -> None: ...
