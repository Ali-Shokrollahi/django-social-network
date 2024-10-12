import pytest
from django.core.exceptions import ValidationError

from apps.users.models import Follow
from apps.users.services.profile import ProfileService
from apps.users.services.subscription import SubscriptionService


@pytest.mark.django_db
def test_update_profile(profile):
    updated_profile = ProfileService.update_profile(profile, "new name", "new lastname", "new bio")

    profile.refresh_from_db()

    assert profile.first_name == "new name"
    assert profile.last_name == "new lastname"
    assert profile.bio == "new bio"

    assert updated_profile.first_name == profile.first_name
    assert updated_profile.last_name == profile.last_name
    assert updated_profile.bio == profile.bio


def test_update_username(profile):
    ProfileService.update_username(profile, "new username")
    profile.refresh_from_db()
    assert profile.username == "new username"


def test_follow_success(profile, another_profile):
    service = SubscriptionService()
    service.follow(follower=profile, following=another_profile)

    assert Follow.objects.filter(follower=profile, following=another_profile).exists()

    assert profile.following_count == 1
    assert another_profile.follower_count == 1


def test_follow_already_exists(profile, another_profile, follow_relationship):
    service = SubscriptionService()

    with pytest.raises(ValidationError):
        service.follow(follower=profile, following=another_profile)

    follow_count = Follow.objects.filter(follower=profile, following=another_profile).count()
    assert follow_count == 1


def test_unfollow_success(profile, another_profile, follow_relationship):
    service = SubscriptionService()

    service.unfollow(subscription=follow_relationship)

    assert not Follow.objects.filter(follower=profile, following=another_profile).exists()

    assert profile.following_count == 0
    assert another_profile.follower_count == 0
