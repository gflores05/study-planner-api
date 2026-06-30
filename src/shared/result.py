from dataclasses import dataclass

from src.shared.option import Option


@dataclass
class Unit:
  pass


class Result[T, E]:
  def __init__(self, is_success: bool, value: T = None, error: E | None = None):
    self._is_success = is_success
    self._value = value
    self._error = error

  @property
  def is_success(self) -> bool:
    return self._is_success

  @property
  def is_failure(self) -> bool:
    return not self._is_success

  @property
  def value(self) -> T:
    if not self._is_success:
      raise Exception("Cannot get value of a failed result")
    return self._value

  @property
  def error(self) -> E:
    if self._error is None:
      raise Exception("Cannot get error of a success result")

    return self._error

  def unwrap_or_raise(self, e: Exception | None = None) -> T:
    if self.is_failure:
      raise (
        e or self.error
        if isinstance(self.error, Exception)
        else Exception("ResultFailed")
      )
    return self.value

  def to_option(self):
    if self.is_success:
      return Option.some(self._value)
    return Option[T].nothing()

  @staticmethod
  def ok(value: T = None) -> "Result":
    return Result(is_success=True, value=value)

  @staticmethod
  def fail(error: E) -> "Result":
    return Result(is_success=False, error=error)
