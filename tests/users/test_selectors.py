import pytest
from django.http import Http404

from apps.users.selectors.profiles import ProfileSelector


@pytest.mark.django_db
def test_get_profile_success(profile):
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
