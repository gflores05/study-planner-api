from datetime import timedelta

import pytest

from src.application.dtos.user import (
  ChangePasswordRequestDTO,
  LoginRequestDTO,
  RefreshTokenRequestDTO,
  RegisterUserRequestDTO,
)
from src.application.use_cases.user.authenticate_user_use_case import (
  AuthenticateUserUseCaseAdapter,
)
from src.application.use_cases.user.change_password_use_case import (
  ChangePasswordUseCaseAdapter,
)
from src.application.use_cases.user.error import (
  UserAlreadyExists,
  UserInvalidCredentials,
  UserInvalidInputError,
  UserInvalidToken,
  UserNotFoundError,
)
from src.application.use_cases.user.login_use_case import LoginUseCaseAdapter
from src.application.use_cases.user.refresh_token_use_case import (
  RefreshTokenUseCaseAdapter,
)
from src.application.use_cases.user.register_user_use_case import (
  RegisterUserUseCaseAdapter,
)
from src.application.use_cases.user.tokens import ACCESS, REFRESH, build_claims
from src.domain.user.domain_events import (
  UserLoggedIn,
  UserPasswordChanged,
  UserRegistered,
)
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.user_id import UserId
from src.infrastructure.adapters.outbound.auth.jwt_token_service import (
  JwtTokenService,
)
from src.util.date_util import utc_now
from tests.conftest import JANE_EMAIL, JANE_PASSWORD, UserScenario

NEW_PASSWORD = "an0ther-passw0rd"


def _register_use_case(s: UserScenario) -> RegisterUserUseCaseAdapter:
  return RegisterUserUseCaseAdapter(
    user_repository=s.user_repository,
    user_lookup=s.user_lookup,
    password_hasher=s.password_hasher,
  )


def _login_use_case(s: UserScenario) -> LoginUseCaseAdapter:
  return LoginUseCaseAdapter(
    user_repository=s.user_repository,
    user_lookup=s.user_lookup,
    password_hasher=s.password_hasher,
    token_service=s.token_service,
    token_settings=s.token_settings,
  )


def _refresh_use_case(s: UserScenario) -> RefreshTokenUseCaseAdapter:
  return RefreshTokenUseCaseAdapter(
    user_repository=s.user_repository,
    token_service=s.token_service,
    token_settings=s.token_settings,
  )


def _authenticate_use_case(s: UserScenario) -> AuthenticateUserUseCaseAdapter:
  return AuthenticateUserUseCaseAdapter(
    user_repository=s.user_repository, token_service=s.token_service
  )


def _change_password_use_case(s: UserScenario) -> ChangePasswordUseCaseAdapter:
  return ChangePasswordUseCaseAdapter(
    user_repository=s.user_repository, password_hasher=s.password_hasher
  )


# --- Register ---


async def test_register_stores_a_hashed_password(user_scenario: UserScenario):
  response = await _register_use_case(user_scenario).execute(
    RegisterUserRequestDTO(
      email="John@Example.com", name="John", password="pa55word-long"
    )
  )

  user = user_scenario.store.users[UserId.parse(response.id).unwrap_or_raise()]
  assert str(user.email) == "john@example.com"
  assert b"pa55word-long" not in user.password.value
  assert user_scenario.password_hasher.verify("pa55word-long", user.password)
  assert [type(e) for e in user_scenario.store.published_events] == [UserRegistered]


async def test_register_rejects_an_existing_email_ignoring_case(
  user_scenario: UserScenario,
):
  with pytest.raises(UserAlreadyExists):
    await _register_use_case(user_scenario).execute(
      RegisterUserRequestDTO(
        email=JANE_EMAIL.upper(), name="Jane", password="pa55word-long"
      )
    )


@pytest.mark.parametrize(
  ("email", "name", "password", "field"),
  [
    ("not-an-email", "John", "pa55word-long", "Email"),
    ("john@example.com", "  ", "pa55word-long", "Name"),
    ("john@example.com", "John", "short", "Password"),
  ],
)
async def test_register_rejects_invalid_input(
  user_scenario: UserScenario, email: str, name: str, password: str, field: str
):
  with pytest.raises(UserInvalidInputError) as excinfo:
    await _register_use_case(user_scenario).execute(
      RegisterUserRequestDTO(email=email, name=name, password=password)
    )

  assert excinfo.value.field == field
  assert excinfo.value.value != password


# --- Login ---


async def test_login_returns_access_and_refresh_tokens(user_scenario: UserScenario):
  response = await _login_use_case(user_scenario).execute(
    LoginRequestDTO(email=JANE_EMAIL, password=JANE_PASSWORD)
  )

  access = user_scenario.token_service.decode(response.access_token).get()
  refresh = user_scenario.token_service.decode(response.refresh_token).get()
  jane = user_scenario.jane

  assert access["sub"] == refresh["sub"] == str(jane.id)
  assert access["email"] == JANE_EMAIL
  assert (access["type"], refresh["type"]) == (ACCESS, REFRESH)
  assert access["exp"] - access["iat"] == 15 * 60
  assert refresh["exp"] - refresh["iat"] == 7 * 24 * 60 * 60
  assert jane.last_login_on.is_some
  assert [type(e) for e in user_scenario.store.published_events] == [UserLoggedIn]


@pytest.mark.parametrize(
  ("email", "password"),
  [
    (JANE_EMAIL, "wrong-password"),
    ("unknown@example.com", JANE_PASSWORD),
    ("not-an-email", JANE_PASSWORD),
  ],
)
async def test_login_rejects_bad_credentials(
  user_scenario: UserScenario, email: str, password: str
):
  with pytest.raises(UserInvalidCredentials):
    await _login_use_case(user_scenario).execute(
      LoginRequestDTO(email=email, password=password)
    )


async def test_login_rejects_an_inactive_user(user_scenario: UserScenario):
  user_scenario.jane.deactivate(utc_now())

  with pytest.raises(UserInvalidCredentials):
    await _login_use_case(user_scenario).execute(
      LoginRequestDTO(email=JANE_EMAIL, password=JANE_PASSWORD)
    )


# --- Refresh ---


def _token(s: UserScenario, type: str, expires_in=timedelta(minutes=5)) -> str:
  return s.token_service.encode(build_claims(s.jane, type), expires_in)


async def test_refresh_returns_a_new_access_token(user_scenario: UserScenario):
  response = await _refresh_use_case(user_scenario).execute(
    RefreshTokenRequestDTO(refresh_token=_token(user_scenario, REFRESH))
  )

  claims = user_scenario.token_service.decode(response.access_token).get()
  assert claims["type"] == ACCESS
  assert claims["sub"] == str(user_scenario.jane.id)


@pytest.mark.parametrize(
  "make_token",
  [
    pytest.param(lambda s: _token(s, ACCESS), id="access token"),
    pytest.param(
      lambda s: _token(s, REFRESH, expires_in=timedelta(seconds=-1)), id="expired"
    ),
    pytest.param(
      lambda s: JwtTokenService("another-secret-key-at-least-32-bytes").encode(
        build_claims(s.jane, REFRESH), timedelta(minutes=5)
      ),
      id="other key",
    ),
    pytest.param(lambda s: "garbage", id="garbage"),
  ],
)
async def test_refresh_rejects_invalid_tokens(user_scenario: UserScenario, make_token):
  with pytest.raises(UserInvalidToken):
    await _refresh_use_case(user_scenario).execute(
      RefreshTokenRequestDTO(refresh_token=make_token(user_scenario))
    )


async def test_refresh_rejects_a_token_of_an_unknown_user(user_scenario: UserScenario):
  token = _token(user_scenario, REFRESH)
  user_scenario.store.users.clear()

  with pytest.raises(UserInvalidToken):
    await _refresh_use_case(user_scenario).execute(
      RefreshTokenRequestDTO(refresh_token=token)
    )


# --- Authenticate ---


async def test_authenticate_returns_the_token_user(user_scenario: UserScenario):
  user = await _authenticate_use_case(user_scenario).execute(
    _token(user_scenario, ACCESS)
  )

  assert user.id == user_scenario.jane.id


async def test_authenticate_rejects_a_refresh_token(user_scenario: UserScenario):
  with pytest.raises(UserInvalidToken):
    await _authenticate_use_case(user_scenario).execute(_token(user_scenario, REFRESH))


async def test_authenticate_rejects_an_inactive_user(user_scenario: UserScenario):
  user_scenario.jane.deactivate(utc_now())

  with pytest.raises(UserInvalidToken):
    await _authenticate_use_case(user_scenario).execute(_token(user_scenario, ACCESS))


# --- Change password ---


async def test_change_password(user_scenario: UserScenario):
  jane = user_scenario.jane

  await _change_password_use_case(user_scenario).execute(
    user_id=str(jane.id),
    dto=ChangePasswordRequestDTO(
      current_password=JANE_PASSWORD, new_password=NEW_PASSWORD
    ),
  )

  assert user_scenario.password_hasher.verify(NEW_PASSWORD, jane.password)
  assert not user_scenario.password_hasher.verify(JANE_PASSWORD, jane.password)
  assert [type(e) for e in user_scenario.store.published_events] == [
    UserPasswordChanged
  ]


async def test_change_password_rejects_a_wrong_current_password(
  user_scenario: UserScenario,
):
  with pytest.raises(UserInvalidCredentials):
    await _change_password_use_case(user_scenario).execute(
      user_id=str(user_scenario.jane.id),
      dto=ChangePasswordRequestDTO(
        current_password="wrong-password", new_password=NEW_PASSWORD
      ),
    )


async def test_change_password_rejects_a_weak_new_password(
  user_scenario: UserScenario,
):
  with pytest.raises(UserInvalidInputError) as excinfo:
    await _change_password_use_case(user_scenario).execute(
      user_id=str(user_scenario.jane.id),
      dto=ChangePasswordRequestDTO(current_password=JANE_PASSWORD, new_password="x"),
    )

  assert excinfo.value.field == "NewPassword"
  assert user_scenario.password_hasher.verify(
    JANE_PASSWORD, user_scenario.jane.password
  )


async def test_change_password_rejects_an_unknown_user(user_scenario: UserScenario):
  with pytest.raises(UserNotFoundError):
    await _change_password_use_case(user_scenario).execute(
      user_id=str(UserId.create()),
      dto=ChangePasswordRequestDTO(
        current_password=JANE_PASSWORD, new_password=NEW_PASSWORD
      ),
    )


async def test_lookup_is_by_normalized_email(user_scenario: UserScenario):
  found = await user_scenario.user_lookup.get_by_email(
    Email.parse(" JANE.DOE@example.com").unwrap_or_raise()
  )

  assert found.is_some
