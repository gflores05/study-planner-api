from src.application.dtos.user import CreateUserRequestDTO, CreateUserResponseDTO
from src.application.ports.outbound.lookups.user_lookup import UserLookupPort
from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.use_cases.user.error import (
  UserAlreadyExists,
  UserInvalidInputError,
)
from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.external_id import ExternalId
from src.domain.user.value_objects.name import Name
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.option import Option
from src.util.date_util import utc_now


class CreateUserUseCaseAdapter:
  def __init__(self, user_repository: UserRepository, user_lookup: UserLookupPort):
    self.user_repository = user_repository
    self.user_lookup = user_lookup

  async def execute(self, dto: CreateUserRequestDTO) -> CreateUserResponseDTO:
    external_id = ExternalId.parse(dto.auth0_id).unwrap_or_map_and_raise(
      lambda e: UserInvalidInputError(value=dto.auth0_id, field="ExternalId")
    )

    existing = await self.user_lookup.get_by_external_id(external_id)

    if existing.is_some:
      raise UserAlreadyExists(external_id=dto.auth0_id)

    user = User.create(
      external_id=external_id,
      email=Email.parse(dto.email).unwrap_or_map_and_raise(
        lambda e: UserInvalidInputError(value=dto.email, field="Email")
      ),
      name=Name.parse(dto.name).unwrap_or_map_and_raise(
        lambda e: UserInvalidInputError(value=dto.name, field="Name")
      ),
      picture=Option.of(
        NonEmptyString.parse(dto.picture).unwrap_or_map_and_raise(
          lambda e: UserInvalidInputError(value=dto.picture, field="Picture")
        )
      )
      if dto.picture is not None
      else Option.nothing(),
      provider=NonEmptyString.parse(dto.provider).unwrap_or_map_and_raise(
        lambda e: UserInvalidInputError(value=dto.provider, field="Provider")
      ),
    )

    # This should be call in a new use case after the use verifies his email
    user.activate(utc_now())

    await self.user_repository.save(user=user)

    return CreateUserResponseDTO(id=str(user.id))
