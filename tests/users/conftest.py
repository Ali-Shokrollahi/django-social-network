import pytest
from rest_framework.test import APIClient

from apps.users.models import Profile, Follow
from apps.users.services.subscription import SubscriptionService


@pytest.fixture
def api_client():
    """Fixture to provide API client."""
    return APIClient()


@pytest.fixture
def profile_data():
    return {
        "username": "test_user",
        "first_name": "test firstname",
        "last_name": "test lastname",
        "bio": "test bio"
    }


@pytest.fixture
def user(django_user_model):
    """Fixture to create and return a user."""
    return django_user_model.objects.create_user(email="testuser@email.com", password="Test@1pass")


@pytest.fixture
def profile(user, profile_data):
    """Fixture to create and return a profile."""
    return Profile.objects.create(user=user, **profile_data)


@pytest.fixture
def another_user(django_user_model):
    """Fixture to create another user."""
    return django_user_model.objects.create_user(email="otheruser@email.com", password="Test@1pass")


@pytest.fixture
def another_profile(another_user):
    """Fixture to create another user's profile."""
    return Profile.objects.create(user=another_user, username="other_user", first_name="other first_name",
                                  last_name="other last_name",
                                  bio="other bio")


@pytest.fixture
def follow_relationship(profile, another_profile):
    return SubscriptionService().follow(follower=profile, following=another_profile)
