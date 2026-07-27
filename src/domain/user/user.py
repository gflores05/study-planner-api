from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.external_id import ExternalId
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.user_id import UserId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.aggregate_root import AggregateRoot
from src.shared.option import Option


class UserStatus(Enum):
  PENDING = "PENDING"
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"
  UNKNOWN = "UNKNOWN"


@dataclass(kw_only=True)
class User(AggregateRoot[UserId]):
  external_id: ExternalId
  email: Email
  name: Name
  picture: Option[NonEmptyString]
  provider: NonEmptyString
  status: UserStatus

  @staticmethod
  def create(
    external_id: ExternalId,
    email: Email,
    name: Name,
    picture: Option[NonEmptyString],
    provider: NonEmptyString,
  ):
    return User(
      id=UserId.create(),
      external_id=external_id,
      email=email,
      name=name,
      picture=picture,
      provider=provider,
      status=UserStatus.PENDING,
    )

  @staticmethod
  def reconstitute(
    id: UserId,
    created_on: datetime,
    modified_on: datetime,
    version: int,
    external_id: ExternalId,
    email: Email,
    name: Name,
    picture: Option[NonEmptyString],
    provider: NonEmptyString,
    status: UserStatus,
  ):
    return User(
      id=id,
      created_on=created_on,
      modified_on=modified_on,
      version=version,
      external_id=external_id,
      email=email,
      name=name,
      picture=picture,
      provider=provider,
      status=status,
    )

  def activate(self, activated_on: datetime):
    self.modified_on = activated_on
    self.status = UserStatus.ACTIVE

  def deactivate(self, deactivated_on: datetime):
    self.modified_on = deactivated_on
    self.status = UserStatus.INACTIVE
