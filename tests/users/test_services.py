import pytest

from apps.users.services.profile import ProfileService


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
