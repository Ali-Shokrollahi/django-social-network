import pytest

from apps.accounts.services.registration import RegistrationService



@pytest.fixture
def registration_service():
    return RegistrationService


@pytest.fixture
def user_data():
    return {
        'email': 'testuser@email.com',
        'username': 'test_user',
        'password': 'Test@1pass'
    }




