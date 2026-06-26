from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class Subject:
  value: str

  @staticmethod
  def create(value: str) -> Result["Subject"]:
    if len(value) == 0:
      return Result.fail("The subject cannot be empty")

    return Result.ok(Subject(value=value))

  def __str__(self) -> str:
    return self.value
