from typing import Protocol

from src.application.dtos.user import CreateUserRequestDTO, CreateUserResponseDTO


class CreateUserUseCasePort(Protocol):
  async def execute(self, dto: CreateUserRequestDTO) -> CreateUserResponseDTO: ...
