from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.shared.domain_event_id import DomainEventId


@dataclass(frozen=True)
class DomainEvent:
  event_name: str
  event_id: DomainEventId = DomainEventId.create()
  occurred_on: datetime = field(default_factory=lambda: datetime.now(UTC))
