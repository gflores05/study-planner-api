from typing import Protocol

from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.shared.option import Option


class UserLookupPort(Protocol):
  async def get_by_email(self, email: Email) -> Option[User]: ...
