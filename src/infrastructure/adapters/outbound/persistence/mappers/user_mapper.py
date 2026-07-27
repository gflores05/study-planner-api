import uuid

from src.domain.user.user import User, UserStatus
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.external_id import ExternalId
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.user_id import UserId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.infrastructure.adapters.outbound.persistence.models.user_model import UserModel
from src.shared.option import Option


def map_user_model_to_domain(model: UserModel) -> User:
  return User.reconstitute(
    id=UserId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    external_id=ExternalId.parse(model.external_id).unwrap_or_raise(),
    email=Email.parse(model.email).unwrap_or_raise(),
    name=Name.parse(model.name).unwrap_or_raise(),
    picture=Option.of(NonEmptyString.parse(model.picture).unwrap_or_raise())
    if model.picture is not None
    else Option.nothing(),
    provider=NonEmptyString.parse(model.provider).unwrap_or_raise(),
    status=map_user_model_status_to_domain(model.status),
  )


def map_user_domain_to_model(domain: User) -> UserModel:
  return UserModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    external_id=str(domain.external_id),
    email=str(domain.email),
    name=str(domain.name),
    picture=str(domain.picture),
    provider=str(domain.provider),
    status=domain.status.value,
  )


def map_user_model_status_to_domain(status: str) -> UserStatus:
  match status:
    case "ACTIVATE":
      return UserStatus.ACTIVE
    case "INACTIVE":
      return UserStatus.INACTIVE
    case "PENDING":
      return UserStatus.PENDING

  return UserStatus.UNKNOWN
