import pytest

from apps.users.models import Profile
from apps.users.services.subscription import SubscriptionService


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
