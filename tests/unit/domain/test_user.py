from datetime import timedelta

import pytest

from src.domain.user.domain_events import (
  UserLoggedIn,
  UserPasswordChanged,
  UserRegistered,
)
from src.domain.user.problems import UserInvalidStatusProblem
from src.domain.user.user import User, UserStatus
from src.domain.user.value_objects.email import Email
from src.domain.user.value_objects.hashed_password import HashedPassword
from src.domain.user.value_objects.name import Name
from src.domain.user.value_objects.password import Password
from src.util.date_util import utc_now


def _register() -> User:
  return User.register(
    email=Email.parse("jane.doe@example.com").unwrap_or_raise(),
    name=Name.parse("Jane Doe").unwrap_or_raise(),
    password=HashedPassword(value=b"hash"),
    registered_on=utc_now(),
  )


def test_register_creates_an_active_user_and_emits_user_registered():
  user = _register()

  assert user.status == UserStatus.ACTIVE
  assert user.last_login_on.is_nothing
  assert len(user.domain_events) == 1
  event = user.domain_events[0]
  assert isinstance(event, UserRegistered)
  assert event.user_id == str(user.id)
  assert event.email == "jane.doe@example.com"


def test_change_password_replaces_the_hash_and_emits_user_password_changed():
  user = _register()
  user.clear_domain_events()
  changed_on = utc_now() + timedelta(minutes=1)

  user.change_password(HashedPassword(value=b"new-hash"), changed_on=changed_on)

  assert user.password == HashedPassword(value=b"new-hash")
  assert user.modified_on == changed_on
  assert [type(e) for e in user.domain_events] == [UserPasswordChanged]


def test_login_records_the_login_and_emits_user_logged_in():
  user = _register()
  user.clear_domain_events()
  logged_in_on = utc_now()

  result = user.login(logged_in_on=logged_in_on)

  assert result.is_success
  assert user.last_login_on.get() == logged_in_on
  assert [type(e) for e in user.domain_events] == [UserLoggedIn]


def test_login_fails_for_an_inactive_user():
  user = _register()
  user.deactivate(utc_now())
  user.clear_domain_events()

  result = user.login(logged_in_on=utc_now())

  assert result.is_failure
  assert isinstance(result.error, UserInvalidStatusProblem)
  assert user.last_login_on.is_nothing
  assert user.domain_events == []


def test_domain_events_get_unique_ids():
  assert _register().domain_events[0].event_id != _register().domain_events[0].event_id


@pytest.mark.parametrize("value", ["12345678", "x" * 128])
def test_password_accepts_valid_lengths(value: str):
  assert Password.parse(value).is_success


@pytest.mark.parametrize("value", [None, "", "1234567", "x" * 129])
def test_password_rejects_invalid_lengths(value: str | None):
  result = Password.parse(value)

  assert result.is_failure
  assert result.error.value is None  # never echoes the password


def test_password_is_redacted():
  password = Password.parse("s3cret-passw0rd").unwrap_or_raise()

  assert "s3cret" not in repr(password)
  assert "s3cret" not in str(password)


def test_email_is_normalized():
  assert str(Email.parse("  Jane.Doe@Example.COM ").unwrap_or_raise()) == (
    "jane.doe@example.com"
  )


@pytest.mark.parametrize("value", [None, "", "jane", "jane@", "@example.com"])
def test_email_rejects_invalid_values(value: str | None):
  assert Email.parse(value).is_failure


@pytest.mark.parametrize("value", [None, "", "   ", "x" * 101])
def test_name_rejects_invalid_values(value: str | None):
  assert Name.parse(value).is_failure
