from unittest.mock import patch

import pytest

from apps.accounts.exceptions import UserAlreadyActivatedException
from apps.accounts.services.registration import EmailConfirmationToken
from apps.users.models import Profile


@pytest.mark.django_db
@patch('apps.accounts.services.registration.EmailMessage.send')
def test_register_user(mock_send_email, registration_service, user_data):
    user, tokens = registration_service().register(**user_data)

    # Assert the user was created
    assert user.email == user_data['email']
    assert user.check_password(user_data['password'])

    # Assert profile was created
    assert Profile.objects.filter(user=user, username=user_data['username']).exists()

    # Assert that the token contains refresh and access keys
    assert 'refresh' in tokens
    assert 'access' in tokens

    # Assert that the email was sent
    mock_send_email.assert_called_once()


@pytest.mark.django_db
def test_activate_user(registration_service, user_factory):
    user = user_factory()
    token = EmailConfirmationToken.for_user(user)

    registration_service().activate_user(token=str(token))

    user.refresh_from_db()
    assert user.is_active
    assert user.is_verified


@pytest.mark.django_db
def test_activate_user_already_activated(registration_service, user_factory):
    user = user_factory()
    user.is_active = True
    user.is_verified = True
    user.save()

    token = EmailConfirmationToken.for_user(user)

    with pytest.raises(UserAlreadyActivatedException) as exc_info:
        registration_service().activate_user(token=str(token))

    assert str(exc_info.value) == 'This account is already activated.'
