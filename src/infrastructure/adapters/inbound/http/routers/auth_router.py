from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.application.dtos.user import (
  AccessTokenResponseDTO,
  LoginRequestDTO,
  RefreshTokenRequestDTO,
  RegisterUserRequestDTO,
  RegisterUserResponseDTO,
  TokenResponseDTO,
)
from src.application.ports.inbound.user.login_use_case import LoginUseCasePort
from src.application.ports.inbound.user.refresh_token_use_case import (
  RefreshTokenUseCasePort,
)
from src.application.ports.inbound.user.register_user_use_case import (
  RegisterUserUseCasePort,
)
from src.infrastructure.config.container import Container

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post(
  "/register",
  response_model=RegisterUserResponseDTO,
  status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
  body: RegisterUserRequestDTO,
  use_case: Annotated[
    RegisterUserUseCasePort, Depends(Provide[Container.register_user_use_case])
  ],
) -> RegisterUserResponseDTO:
  return await use_case.execute(dto=body)


@router.post("/login", response_model=TokenResponseDTO)
@inject
async def login(
  body: LoginRequestDTO,
  use_case: Annotated[LoginUseCasePort, Depends(Provide[Container.login_use_case])],
) -> TokenResponseDTO:
  return await use_case.execute(dto=body)


@router.post("/refresh", response_model=AccessTokenResponseDTO)
@inject
async def refresh(
  body: RefreshTokenRequestDTO,
  use_case: Annotated[
    RefreshTokenUseCasePort, Depends(Provide[Container.refresh_token_use_case])
  ],
) -> AccessTokenResponseDTO:
  return await use_case.execute(dto=body)
