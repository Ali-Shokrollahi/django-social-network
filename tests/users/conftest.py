import pytest

from apps.users.services.profile import ProfileService
from apps.users.services.subscription import SubscriptionService


@pytest.fixture
def profile_service():
    return ProfileService


@pytest.fixture
def subscription_service():
    return SubscriptionService
