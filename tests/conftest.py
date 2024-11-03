import pytest
from rest_framework.test import APIClient

from .factories import UserFactory, ProfileFactory, FollowFactory


@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def profile_factory():
    return ProfileFactory


@pytest.fixture
def follow_factory():
    return FollowFactory


@pytest.fixture
def api_client():
    """Fixture to provide API client."""
    return APIClient()


@pytest.fixture
def authenticated_client():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user)
    return client
