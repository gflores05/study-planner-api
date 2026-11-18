from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class TokenSettings:
  """How long the tokens issued by the auth use cases are valid."""

  access_token_expires_in: timedelta
  refresh_token_expires_in: timedelta
