from dataclasses import asdict
from typing import Any, Type

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON, TypeDecorator


class DataclassJSONB[T](TypeDecorator):
  """Transparently serializes/deserializes a dataclass to a PostgreSQL JSONB column."""

  impl = JSONB
  cache_ok = True

  def __init__(self, dataclass_type: Type[T], *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dataclass_type = dataclass_type

  def process_bind_param(self, value, dialect):
    """Convert dataclass to dict when saving to the database."""
    if value is None:
      return None
    # If it is already a dict, return it; otherwise, extract fields
    return asdict(value) if hasattr(value, "__dataclass_fields__") else value

  def process_result_value(self, value, dialect):
    """Convert dict back to dataclass when loading from the database."""
    if value is None:
      return None
    # Unpack the dictionary into the dataclass constructor
    return self.dataclass_type(**value)


class JSONBDataClassArray(TypeDecorator):
  """Maps a PostgreSQL JSONB array to a list of dataclasses."""

  impl = JSON
  cache_ok = True

  def __init__(self, dataclass_cls: Any, *args: Any, **kwargs: Any):
    super().__init__(*args, **kwargs)
    self.dataclass_cls = dataclass_cls

  def process_bind_param(self, value: Any, dialect: Any) -> Any:
    # Convert list of dataclasses to a list of dictionaries for the database
    if value is None:
      return None
    return [asdict(obj) for obj in value]

  def process_result_value(self, value: Any, dialect: Any) -> Any:
    # Convert list of dictionaries from the database back to dataclasses
    if value is None:
      return None
    return [self.dataclass_cls(**item) for item in value]
