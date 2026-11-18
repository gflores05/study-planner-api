from typing import Protocol

from src.application.dtos.user import ChangePasswordRequestDTO


class ChangePasswordUseCasePort(Protocol):
  async def execute(self, user_id: str, dto: ChangePasswordRequestDTO) -> None: ...
