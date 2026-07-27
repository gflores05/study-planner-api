from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class ExternalId:
  value: str

  @staticmethod
  def parse(value: str) -> Result["ExternalId", ValidationError]:
    if value is None or len(value) == 0:
      return Result.fail(ValidationError("InvalidExternalId", value=value))

    return Result.ok(ExternalId(value=value))

  def __str__(self) -> str:
    return self.value
