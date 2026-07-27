from dataclasses import dataclass
from uuid import uuid4

from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.string_util import is_valid_uuid


@dataclass(frozen=True)
class UserId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["UserId", ValidationError]:
    if not is_valid_uuid(value):
      return Result.fail(ValidationError("InvalidUUID", value=value))

    return Result.ok(UserId(value=value))

  @staticmethod
  def create() -> "UserId":
    return UserId(value=str(uuid4()))

  def __str__(self) -> str:
    return self.value
