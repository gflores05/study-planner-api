from dataclasses import dataclass, field

from src.shared.result import Result
from src.shared.validation_error import ValidationError

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 32


@dataclass(frozen=True)
class Password:
  """A plaintext password that satisfies the password policy.

  It only lives in memory while it is being hashed or verified, it is never
  persisted and it is redacted from any representation.
  """

  value: str = field(repr=False)

  @staticmethod
  def parse(value: str | None) -> Result[Password, ValidationError]:
    if value is None or not (MIN_PASSWORD_LENGTH <= len(value) <= MAX_PASSWORD_LENGTH):
      # The rejected value is not echoed back to avoid leaking it in errors/logs.
      return Result.fail(ValidationError("InvalidPassword", value=None))

    return Result.ok(Password(value=value))

  def __str__(self) -> str:
    return "********"
