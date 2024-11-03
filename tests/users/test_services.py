import pytest
from django.core.exceptions import ValidationError

from apps.users.models import Follow
from apps.users.services.profile import ProfileService
from apps.users.services.subscription import SubscriptionService


@pytest.mark.django_db
def test_update_profile(profile_factory, profile_service):
    profile = profile_factory()
    updated_profile = profile_service.update_profile(profile, "new name", "new lastname", "new bio")

    profile.refresh_from_db()

    assert profile.first_name == "new name"
    assert profile.last_name == "new lastname"
    assert profile.bio == "new bio"

    assert updated_profile.first_name == profile.first_name
    assert updated_profile.last_name == profile.last_name
    assert updated_profile.bio == profile.bio


@pytest.mark.django_db
def test_update_username(profile_factory, profile_service):
    profile = profile_factory()
    profile_service.update_username(profile, "new username")
    profile.refresh_from_db()
    assert profile.username == "new username"


@pytest.mark.django_db
def test_follow_success(profile_factory, subscription_service):
    profile = profile_factory()
    another_profile = profile_factory()
    subscription_service().follow(follower=profile, following=another_profile)

    assert Follow.objects.filter(follower=profile, following=another_profile).exists()

    assert profile.following_count == 1
    assert another_profile.follower_count == 1


@pytest.mark.django_db
def test_follow_already_exists(profile_factory, follow_factory, subscription_service):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_factory(follower=profile, following=another_profile)

    with pytest.raises(ValidationError):
        subscription_service().follow(follower=profile, following=another_profile)

    follow_count = Follow.objects.filter(follower=profile, following=another_profile).count()
    assert follow_count == 1


@pytest.mark.django_db
def test_unfollow_success(profile_factory, follow_factory, subscription_service):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_relationship = subscription_service().follow(follower=profile, following=another_profile)

    subscription_service().unfollow(subscription=follow_relationship)

    assert not Follow.objects.filter(follower=profile, following=another_profile).exists()

    assert profile.following_count == 0
    assert another_profile.follower_count == 0
