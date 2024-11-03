import pytest
from django.http import Http404

from apps.users.selectors.profiles import ProfileSelector
from apps.users.selectors.subscription import SubscriptionSelector


@pytest.mark.django_db
def test_get_profile_success(profile_factory):
    profile = profile_factory()
    selector = ProfileSelector(username=profile.username)

    fetched_profile = selector.get_profile()

    assert fetched_profile == profile
    assert fetched_profile.username == profile.username
    assert fetched_profile.first_name == profile.first_name
    assert fetched_profile.last_name == profile.last_name
    assert fetched_profile.bio == profile.bio


@pytest.mark.django_db
def test_get_profile_not_found():
    selector = ProfileSelector(username="nonexistentuser")

    with pytest.raises(Http404):
        selector.get_profile()


@pytest.mark.django_db
def test_get_subscription_success(profile_factory, follow_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_factory(follower=profile, following=another_profile)
    subscription = SubscriptionSelector.get_subscription(follower=profile, following=another_profile)

    assert subscription is not None
    assert subscription.follower == profile
    assert subscription.following == another_profile


@pytest.mark.django_db
def test_get_subscription_not_found(profile_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    with pytest.raises(Http404):
        SubscriptionSelector.get_subscription(follower=profile, following=another_profile)


@pytest.mark.django_db
def test_get_profile_followers_success(profile_factory, follow_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_relationship = follow_factory(follower=profile, following=another_profile)
    profile_username = follow_relationship.following.username
    followers = ProfileSelector(username=profile_username).get_profile_followers()
    assert followers.count() == 1
    assert follow_relationship.follower in followers


@pytest.mark.django_db
def test_get_profile_followings_success(profile_factory, follow_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_relationship = follow_factory(follower=profile, following=another_profile)
    profile_username = follow_relationship.follower.username
    followings = ProfileSelector(username=profile_username).get_profile_following()
    assert followings.count() == 1
    assert follow_relationship.following in followings
