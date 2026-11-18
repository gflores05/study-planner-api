from typing import Protocol

from src.domain.user.user import User


class AuthenticateUserUseCasePort(Protocol):
  async def execute(self, access_token: str) -> User: ...
