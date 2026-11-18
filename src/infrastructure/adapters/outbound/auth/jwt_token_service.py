from datetime import timedelta
from typing import Any

import jwt

from src.shared.option import Option
from src.util.date_util import utc_now

_ALGORITHM = "HS256"


class JwtTokenService:
  def __init__(self, secret_key: str) -> None:
    self._secret_key = secret_key

  def encode(self, claims: dict[str, Any], expires_in: timedelta) -> str:
    issued_on = utc_now()
    return jwt.encode(
      {**claims, "iat": issued_on, "exp": issued_on + expires_in},
      self._secret_key,
      algorithm=_ALGORITHM,
    )

  def decode(self, token: str) -> Option[dict[str, Any]]:
    try:
      return Option.some(jwt.decode(token, self._secret_key, algorithms=[_ALGORITHM]))
    except jwt.PyJWTError:
      return Option.nothing()
