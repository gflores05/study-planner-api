from src.application.dtos.user import UserDTO
from src.domain.user.user import User


def map_user_domain_to_dto(domain: User) -> UserDTO:
  return UserDTO(
    id=str(domain.id),
    name=str(domain.name),
    email=str(domain.email),
  )
