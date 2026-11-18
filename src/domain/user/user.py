from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.domain.user.domain_events import (
  UserLoggedIn,
  UserPasswordChanged,
  UserRegistered,
)
from src.domain.user.problems import UserInvalidStatusProblem, UserProblem
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.hashed_password import HashedPassword
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.user_id import UserId
from src.shared.aggregate_root import AggregateRoot
from src.shared.option import Option
from src.shared.result import Result, Unit


class UserStatus(Enum):
  PENDING = "PENDING"
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"
  UNKNOWN = "UNKNOWN"


@dataclass(kw_only=True)
class User(AggregateRoot[UserId]):
  email: Email
  name: Name
  password: HashedPassword
  status: UserStatus
  last_login_on: Option[datetime]

  @staticmethod
  def register(
    email: Email, name: Name, password: HashedPassword, registered_on: datetime
  ) -> User:
    user = User(
      id=UserId.create(),
      created_on=registered_on,
      modified_on=registered_on,
      email=email,
      name=name,
      password=password,
      status=UserStatus.ACTIVE,
      last_login_on=Option.nothing(),
    )

    user.add_domain_event(
      UserRegistered(
        user_id=str(user.id), email=str(email), registered_on=registered_on
      )
    )

    return user

  @staticmethod
  def reconstitute(
    id: UserId,
    created_on: datetime,
    modified_on: datetime,
    version: int,
    email: Email,
    name: Name,
    password: HashedPassword,
    status: UserStatus,
    last_login_on: Option[datetime],
  ) -> User:
    return User(
      id=id,
      created_on=created_on,
      modified_on=modified_on,
      version=version,
      email=email,
      name=name,
      password=password,
      status=status,
      last_login_on=last_login_on,
    )

  @property
  def is_active(self) -> bool:
    return self.status == UserStatus.ACTIVE

  def change_password(self, password: HashedPassword, changed_on: datetime) -> None:
    self.password = password
    self.modified_on = changed_on
    self.add_domain_event(
      UserPasswordChanged(user_id=str(self.id), changed_on=changed_on)
    )

  def login(self, logged_in_on: datetime) -> Result[Unit, UserProblem]:
    if not self.is_active:
      return Result.fail(
        UserInvalidStatusProblem(
          user_id=str(self.id),
          current_status=self.status.value,
          required_status=UserStatus.ACTIVE.value,
        )
      )

    self.last_login_on = Option.some(logged_in_on)
    self.modified_on = logged_in_on
    self.add_domain_event(UserLoggedIn(user_id=str(self.id), logged_in_on=logged_in_on))

    return Result.ok(Unit)

  def activate(self, activated_on: datetime) -> None:
    self.modified_on = activated_on
    self.status = UserStatus.ACTIVE

  def deactivate(self, deactivated_on: datetime) -> None:
    self.modified_on = deactivated_on
    self.status = UserStatus.INACTIVE
