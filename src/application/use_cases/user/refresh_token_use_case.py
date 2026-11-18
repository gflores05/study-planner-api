from src.application.dtos.auth import TokenSettings
from src.application.dtos.user import AccessTokenResponseDTO, RefreshTokenRequestDTO
from src.application.ports.outbound.repositories.user_repository import UserRepository
from src.application.ports.outbound.security.token_service import TokenServicePort
from src.application.use_cases.user.tokens import (
  ACCESS,
  REFRESH,
  build_claims,
  resolve_token_user,
)


class RefreshTokenUseCaseAdapter:
  def __init__(
    self,
    user_repository: UserRepository,
    token_service: TokenServicePort,
    token_settings: TokenSettings,
  ):
    self.user_repository = user_repository
    self.token_service = token_service
    self.token_settings = token_settings

  async def execute(self, dto: RefreshTokenRequestDTO) -> AccessTokenResponseDTO:
    user = await resolve_token_user(
      token=dto.refresh_token,
      type=REFRESH,
      token_service=self.token_service,
      user_repository=self.user_repository,
    )

    return AccessTokenResponseDTO(
      access_token=self.token_service.encode(
        build_claims(user, ACCESS), self.token_settings.access_token_expires_in
      )
    )
