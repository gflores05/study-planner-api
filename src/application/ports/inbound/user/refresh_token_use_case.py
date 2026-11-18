from typing import Protocol

from src.application.dtos.user import AccessTokenResponseDTO, RefreshTokenRequestDTO


class RefreshTokenUseCasePort(Protocol):
  async def execute(self, dto: RefreshTokenRequestDTO) -> AccessTokenResponseDTO: ...
