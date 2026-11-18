from typing import Protocol

from src.application.dtos.user import RegisterUserRequestDTO, RegisterUserResponseDTO


class RegisterUserUseCasePort(Protocol):
  async def execute(self, dto: RegisterUserRequestDTO) -> RegisterUserResponseDTO: ...
