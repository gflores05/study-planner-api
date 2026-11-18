from typing import Protocol

from src.domain.user.value_objects.hashed_password import HashedPassword
from src.domain.user.value_objects.password import Password


class PasswordHasherPort(Protocol):
  def hash(self, password: Password) -> HashedPassword: ...
  def verify(self, password: str, hashed: HashedPassword) -> bool: ...
