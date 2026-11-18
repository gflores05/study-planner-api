import uuid

from src.domain.user.user import User, UserStatus
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.hashed_password import HashedPassword
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.user_id import UserId
from src.infrastructure.adapters.outbound.persistence.models.user_model import UserModel
from src.shared.option import Option


def map_user_model_to_domain(model: UserModel) -> User:
  return User.reconstitute(
    id=UserId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    email=Email.parse(model.email).unwrap_or_raise(),
    name=Name.parse(model.name).unwrap_or_raise(),
    password=HashedPassword.parse(model.password_hash).unwrap_or_raise(),
    status=map_user_model_status_to_domain(model.status),
    last_login_on=Option.of(model.last_login_on),
  )


def map_user_domain_to_model(domain: User) -> UserModel:
  return UserModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    email=str(domain.email),
    name=str(domain.name),
    password_hash=domain.password.value,
    status=domain.status.value,
    last_login_on=domain.last_login_on.to_nullable(),
  )


def map_user_model_status_to_domain(status: str) -> UserStatus:
  match status:
    case "ACTIVE":
      return UserStatus.ACTIVE
    case "INACTIVE":
      return UserStatus.INACTIVE
    case "PENDING":
      return UserStatus.PENDING

  return UserStatus.UNKNOWN
