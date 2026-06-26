from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class NonEmptyString:
  value: str

  @staticmethod
  def create(value: str) -> Result["NonEmptyString"]:
    if len(value) == 0:
      return Result.fail("The value cannot be empty")

    return Result.ok(NonEmptyString(value=value))

  def __str__(self) -> str:
    return self.value
