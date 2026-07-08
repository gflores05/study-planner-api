from typing import Callable


class Option[T]:
  """
  Represents a value that may or may not be present.
  Replaces None checks with explicit, chainable operations.

  Some(value) — a value is present
  Nothing()   — no value
  """

  def __init__(self, value: T | None):
    self._value = value

  # --- Factories ---
  @staticmethod
  def some(value: T) -> "Option[T]":
    if value is None:
      raise ValueError("Option.some() cannot wrap None — use Option.nothing() instead")
    return Option(value)

  @staticmethod
  def nothing() -> "Option[T]":
    return Option(None)

  @staticmethod
  def of(value: T | None) -> "Option[T]":
    """Smart constructor — wraps a value that may or may not be None."""
    return Option.nothing() if value is None else Option.some(value)

  # --- Checks ---

  @property
  def is_some(self) -> bool:
    return self._value is not None

  @property
  def is_nothing(self) -> bool:
    return self._value is None

  # --- Unwrapping ---

  def get(self) -> T:
    """Returns the value or raises if nothing."""
    if self._value is None:
      raise ValueError("Cannot get value from Nothing")
    return self._value

  def get_or_else(self, default: T) -> T:
    """Returns the value or a default if nothing."""
    return self._value if self._value is not None else default

  def get_or_raise(self, error: Exception) -> T:
    """Returns the value or raises a custom exception if nothing."""
    if self._value is None:
      raise error
    return self._value

  # --- Chaining ---

  def map[U](self, fn: Callable[[T], U]) -> "Option[U]":
    """Transform the value inside if present."""
    if self._value is None:
      return Option.nothing()
    return Option.of(fn(self._value))

  def flat_map[U](self, fn: Callable[[T], "Option[U]"]) -> "Option[U]":
    """Chain operations that themselves return an Option."""
    if self._value is None:
      return Option.nothing()
    return fn(self._value)

  def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
    """Keep the value only if it satisfies the predicate."""
    if self._value is None or not predicate(self._value):
      return Option.nothing()
    return self

  def or_else(self, alternative: "Option[T]") -> "Option[T]":
    """Return self if some, otherwise return the alternative."""
    return self if self.is_some else alternative

  # --- Side effects ---

  def if_some(self, fn: Callable[[T], None]) -> "Option[T]":
    """Run a side effect if value is present. Returns self for chaining."""
    if self._value is not None:
      fn(self._value)
    return self

  def if_nothing(self, fn: Callable[[], None]) -> "Option[T]":
    """Run a side effect if no value. Returns self for chaining."""
    if self.is_nothing:
      fn()
    return self

  def to_nullable(self) -> T | None:
    return self._value

  # --- Dunder ---

  def __repr__(self) -> str:
    return f"Some({self._value!r})" if self.is_some else "Nothing"

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Option):
      return False
    return self._value == other._value

  def __bool__(self) -> bool:
    return self.is_some
