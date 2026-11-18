from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application.ports.inbound.user.authenticate_user_use_case import (
  AuthenticateUserUseCasePort,
)
from src.application.use_cases.user.error import UserInvalidToken
from src.domain.user.user import User
from src.infrastructure.config.container import Container

# auto_error=False so a missing token goes through UserInvalidToken and gets
# the same 401 body as any other auth error.
bearer = HTTPBearer(auto_error=False, description="An `access_token` from `/login`.")


@inject
async def get_user_context(
  credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
  use_case: Annotated[
    AuthenticateUserUseCasePort,
    Depends(Provide[Container.authenticate_user_use_case]),
  ],
) -> User:
  if credentials is None:
    raise UserInvalidToken()

  return await use_case.execute(access_token=credentials.credentials)


CurrentUser = Annotated[User, Depends(get_user_context)]
