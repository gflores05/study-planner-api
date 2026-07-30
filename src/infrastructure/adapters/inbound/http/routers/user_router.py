from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header

from src.application.dtos.user import (
  CreateUserRequestDTO,
  CreateUserResponseDTO,
  UserDTO,
)
from src.application.mappers.user_mapper import map_user_domain_to_dto
from src.application.ports.inbound.user.create_user_use_case import (
  CreateUserUseCasePort,
)
from src.application.use_cases.user.error import UserUnauthorized
from src.domain.user.user import User
from src.infrastructure.adapters.outbound.auth.user_context import get_user_context
from src.infrastructure.config.container import Container
from src.infrastructure.config.settings import Settings

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/webhook/created", response_model=CreateUserResponseDTO)
@inject
async def save_created_user(
  body: CreateUserRequestDTO,
  use_case: Annotated[
    CreateUserUseCasePort, Depends(Provide[Container.create_user_use_case])
  ],
  settings: Annotated[Settings, Depends(Provide[Container.settings])],
  x_webhook_secret: Annotated[str | None, Header()] = None,
) -> CreateUserResponseDTO:
  if x_webhook_secret != settings.auth0_webhook_secret:
    raise UserUnauthorized()

  return await use_case.execute(dto=body)


@router.get("/me", response_model=UserDTO)
async def get_user(
  current: User = Depends(get_user_context),
) -> UserDTO:
  return map_user_domain_to_dto(current)
