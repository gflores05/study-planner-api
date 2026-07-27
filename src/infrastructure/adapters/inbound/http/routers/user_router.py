from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header

from src.application.dtos.user import CreateUserRequestDTO, CreateUserResponseDTO
from src.application.ports.inbound.user.create_user_use_case import (
  CreateUserUseCasePort,
)
from src.application.use_cases.user.error import UserUnauthorized
from src.infrastructure.config.container import Container
from src.infrastructure.config.settings import Settings

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/webhook/created", response_model=CreateUserResponseDTO)
@inject
async def start_assessment(
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
