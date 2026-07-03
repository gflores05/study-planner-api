from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class TopicTitle:
  value: str

  @staticmethod
  def parse(value: str) -> Result["TopicTitle", ValidationError]:
    if len(value) == 0:
      return Result.fail(ValidationError("EmptyTitle", value=value))

    return Result.ok(TopicTitle(value=value))

  def __str__(self) -> str:
    return self.value
