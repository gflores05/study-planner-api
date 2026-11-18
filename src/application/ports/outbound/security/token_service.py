from datetime import timedelta
from typing import Any, Protocol

from src.shared.option import Option


class TokenServicePort(Protocol):
  def encode(self, claims: dict[str, Any], expires_in: timedelta) -> str: ...
  def decode(self, token: str) -> Option[dict[str, Any]]: ...
