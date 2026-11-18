from dataclasses import dataclass, field

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class HashedPassword:
  """The one-way hash of a user's password, as stored in the database."""

  value: bytes = field(repr=False)

  @staticmethod
  def parse(value: bytes | None) -> Result[HashedPassword, ValidationError]:
    if value is None or len(value) == 0:
      return Result.fail(ValidationError("InvalidHashedPassword", value=None))

    return Result.ok(HashedPassword(value=bytes(value)))
