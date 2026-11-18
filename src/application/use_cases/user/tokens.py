from typing import Any, Literal

from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.token_service import TokenServicePort
from src.application.use_cases.user.error import UserInvalidToken
from src.domain.user.user import User
from src.domain.user.value_objects.user_id import UserId

TokenType = Literal["access", "refresh"]

ACCESS: TokenType = "access"
REFRESH: TokenType = "refresh"


def build_claims(user: User, type: TokenType) -> dict[str, Any]:
  return {
    "sub": str(user.id),
    "email": str(user.email),
    "name": str(user.name),
    "type": type,
  }


async def resolve_token_user(
  token: str,
  type: TokenType,
  token_service: TokenServicePort,
  user_repository: UserRepository,
) -> User:
  """Returns the active user a token of the given type was issued to.

  Any problem (bad signature, expired, wrong type, unknown or inactive user)
  is reported as an invalid token so callers can't tell the cases apart.
  """
  claims = token_service.decode(token).get_or_raise(UserInvalidToken())

  if claims.get("type") != type or not isinstance(claims.get("sub"), str):
    raise UserInvalidToken()

  user_id = UserId.parse(claims["sub"]).unwrap_or_map_and_raise(
    lambda e: UserInvalidToken()
  )
  user = (await user_repository.get(user_id)).get_or_raise(UserInvalidToken())

  if not user.is_active:
    raise UserInvalidToken()

  return user
