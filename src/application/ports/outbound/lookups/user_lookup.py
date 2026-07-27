from typing import Protocol

from src.domain.user.user import User
from src.domain.user.value_objects.external_id import ExternalId
from src.shared.option import Option


class UserLookupPort(Protocol):
  async def get_by_external_id(self, id: ExternalId) -> Option[User]: ...
