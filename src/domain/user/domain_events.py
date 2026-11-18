from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain_event import DomainEvent


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
  event_name: str = field(default="UserRegistered")
  user_id: str
  email: str
  registered_on: datetime


@dataclass(frozen=True, kw_only=True)
class UserPasswordChanged(DomainEvent):
  event_name: str = field(default="UserPasswordChanged")
  user_id: str
  changed_on: datetime


@dataclass(frozen=True, kw_only=True)
class UserLoggedIn(DomainEvent):
  event_name: str = field(default="UserLoggedIn")
  user_id: str
  logged_in_on: datetime
