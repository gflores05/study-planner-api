# auth.py
import os

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application.ports.outbound.lookups.user_lookup import UserLookupPort
from src.application.use_cases.user.error import UserNotFoundError
from src.infrastructure.adapters.outbound.auth.token_service import TokenService
from src.infrastructure.config.container import Container

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

security = HTTPBearer()


@inject
async def get_user_context(
  credentials: HTTPAuthorizationCredentials = Depends(security),
  token_service: TokenService = Depends(Provide[Container.token_service]),
  user_lookup: UserLookupPort = Depends(Provide[Container.user_lookup]),
):
  token = credentials.credentials
  payload = token_service.verify(token=token)

  user = await user_lookup.get_by_external_id(payload["sub"])

  return user.get_or_raise(UserNotFoundError(""))
