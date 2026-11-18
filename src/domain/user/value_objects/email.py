import re
from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError

MAX_EMAIL_LENGTH = 320


@dataclass(frozen=True)
class Email:
  value: str

  @staticmethod
  def parse(value: str | None) -> Result[Email, ValidationError]:
    if value is None:
      return Result.fail(ValidationError("InvalidEmail", value=value))

    normalized = value.strip().lower()

    if (
      len(normalized) > MAX_EMAIL_LENGTH
      or re.fullmatch(
        r"^((?!\.)[\w\-_.+]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", normalized
      )
      is None
    ):
      return Result.fail(ValidationError("InvalidEmail", value=value))

    return Result.ok(Email(value=normalized))

  def __str__(self) -> str:
    return self.value
