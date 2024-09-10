import pytest
from rest_framework.test import APIClient

from apps.accounts.services.registration import RegistrationService


@pytest.fixture
def registration_service():
    return RegistrationService()


@pytest.fixture
def user_data():
    return {
        'email': 'testuser@email.com',
        'username': 'test_user',
        'password': 'Test@1pass'
    }


@pytest.fixture
def user1(django_user_model, user_data):
    user = django_user_model.objects.create_user(email=user_data['email'], password=user_data['password'])
    return user


@pytest.fixture
def api_client():
    return APIClient()
