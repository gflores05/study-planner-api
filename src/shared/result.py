from typing import Generic, TypeVar

T = TypeVar("T")


class Result(Generic[T]):
  def __init__(self, is_success: bool, value: T = None, error: str | None = None):
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
  def error(self) -> str:
    if self._error is None:
      raise Exception("Cannot get error of a success result")

    return self._error

  @staticmethod
  def ok(value: T = None) -> "Result[T]":
    return Result(is_success=True, value=value)

  @staticmethod
  def fail(error: str) -> "Result":
    return Result(is_success=False, error=error)
