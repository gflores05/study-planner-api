from dataclasses import dataclass
from datetime import timedelta

import pytest

from src.application.dtos.auth import TokenSettings
from src.domain.user.user import User
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.password import Password
from src.infrastructure.adapters.outbound.auth.jwt_token_service import (
  JwtTokenService,
)
from src.infrastructure.adapters.outbound.auth.pbkdf2_password_hasher import (
  Pbkdf2PasswordHasher,
)
from src.util.date_util import utc_now
from tests.fakes.infrastructure.persistence.repositories.fake_user_repository import (
  FakeUserLookup,
  FakeUserRepository,
  FakeUserStore,
)

JANE_EMAIL = "jane.doe@example.com"
JANE_PASSWORD = "s3cret-passw0rd"
TEST_SECRET_KEY = "test-secret-key-at-least-32-bytes-long!"


@dataclass
class UserScenario:
  jane: User
  store: FakeUserStore
  user_repository: FakeUserRepository
  user_lookup: FakeUserLookup
  password_hasher: Pbkdf2PasswordHasher
  token_service: JwtTokenService
  token_settings: TokenSettings


def make_user(
  hasher: Pbkdf2PasswordHasher,
  email: str = JANE_EMAIL,
  name: str = "Jane Doe",
  password: str = JANE_PASSWORD,
) -> User:
  user = User.register(
    email=Email.parse(email).unwrap_or_raise(),
    name=Name.parse(name).unwrap_or_raise(),
    password=hasher.hash(Password.parse(password).unwrap_or_raise()),
    registered_on=utc_now(),
  )
  user.clear_domain_events()
  return user


@pytest.fixture
def user_scenario() -> UserScenario:
  # Few iterations keep the real hasher fast in tests.
  hasher = Pbkdf2PasswordHasher(iterations=1_000)
  jane = make_user(hasher)
  store = FakeUserStore([jane])

  return UserScenario(
    jane=jane,
    store=store,
    user_repository=FakeUserRepository(store),
    user_lookup=FakeUserLookup(store),
    password_hasher=hasher,
    token_service=JwtTokenService(secret_key=TEST_SECRET_KEY),
    token_settings=TokenSettings(
      access_token_expires_in=timedelta(minutes=15),
      refresh_token_expires_in=timedelta(days=7),
    ),
  )
