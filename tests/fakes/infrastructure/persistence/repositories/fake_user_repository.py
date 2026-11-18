from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.user_id import UserId
from src.shared.domain_event import DomainEvent
from src.shared.option import Option


class FakeUserStore:
  """In-memory users shared by the fake repository and the fake lookup."""

  def __init__(self, users: list[User] | None = None):
    self.users: dict[UserId, User] = {user.id: user for user in users or []}
    self.published_events: list[DomainEvent] = []


class FakeUserRepository:
  def __init__(self, store: FakeUserStore):
    self.store = store

  async def get(self, id: UserId, load_children: bool = True) -> Option[User]:
    return Option.of(self.store.users.get(id))

  async def save(self, user: User) -> None:
    user.increment_version()
    self.store.users[user.id] = user
    self.store.published_events.extend(user.domain_events)
    user.clear_domain_events()


class FakeUserLookup:
  def __init__(self, store: FakeUserStore):
    self.store = store

  async def get_by_email(self, email: Email) -> Option[User]:
    return Option.of(
      next((u for u in self.store.users.values() if u.email == email), None)
    )
