from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.application.dtos.user import ChangePasswordRequestDTO, UserDTO
from src.application.mappers.user_mapper import map_user_domain_to_dto
from src.application.ports.inbound.user.change_password_use_case import (
  ChangePasswordUseCasePort,
)
from src.infrastructure.adapters.inbound.http.security import CurrentUser
from src.infrastructure.config.container import Container

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.get("/me", response_model=UserDTO)
async def get_user(current: CurrentUser) -> UserDTO:
  return map_user_domain_to_dto(current)


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def change_password(
  body: ChangePasswordRequestDTO,
  current: CurrentUser,
  use_case: Annotated[
    ChangePasswordUseCasePort, Depends(Provide[Container.change_password_use_case])
  ],
) -> None:
  await use_case.execute(user_id=str(current.id), dto=body)
