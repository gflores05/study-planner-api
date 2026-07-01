from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar

from src.shared.domain_event import DomainEvent

T = TypeVar("T")


@dataclass
class AggregateRoot(Generic[T]):
  id: T
  created_on: datetime = field(default_factory=lambda: datetime.now(UTC))
  modified_on: datetime = field(default_factory=lambda: datetime.now(UTC))
  version: int = field(default=0)
  _domain_events: list[DomainEvent] = field(default_factory=list, repr=False)

  def add_domain_event(self, event: DomainEvent) -> None:
    self._domain_events.append(event)

  @property
  def domain_events(self) -> list[DomainEvent]:
    return list(self._domain_events)

  def clear_domain_events(self) -> None:
    self._domain_events.clear()
