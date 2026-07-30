from src.application.dtos.user import UserDTO
from src.application.use_cases.user.error import UserInvalidInputError
from src.domain.user.user import User


def map_user_domain_to_dto(domain: User) -> UserDTO:
  return UserDTO(
    id=str(domain.id),
    name=str(domain.name),
    email=str(domain.email),
    picture=str(
      domain.picture.get_or_raise(UserInvalidInputError(value="", field="picture"))
    )
    if domain.picture.is_some
    else None,
  )
