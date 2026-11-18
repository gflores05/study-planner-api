import hashlib
import hmac
import secrets

from src.domain.user.value_objects.hashed_password import HashedPassword
from src.domain.user.value_objects.password import Password

_SALT_LENGTH = 16
_DEFAULT_ITERATIONS = 600_000


class Pbkdf2PasswordHasher:
  """PBKDF2-HMAC-SHA256 with a random per-password salt.

  The stored hash is `salt || digest`, so `verify` can recover the salt.
  """

  def __init__(self, iterations: int = _DEFAULT_ITERATIONS) -> None:
    self.iterations = iterations

  def hash(self, password: Password) -> HashedPassword:
    salt = secrets.token_bytes(_SALT_LENGTH)
    return HashedPassword(value=salt + self._digest(password.value, salt))

  def verify(self, password: str, hashed: HashedPassword) -> bool:
    salt, digest = hashed.value[:_SALT_LENGTH], hashed.value[_SALT_LENGTH:]
    return hmac.compare_digest(self._digest(password, salt), digest)

  def _digest(self, password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt, self.iterations
    )
