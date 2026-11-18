from typing import Protocol

from src.application.dtos.user import LoginRequestDTO, TokenResponseDTO


class LoginUseCasePort(Protocol):
  async def execute(self, dto: LoginRequestDTO) -> TokenResponseDTO: ...
