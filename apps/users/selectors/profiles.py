from django.shortcuts import get_object_or_404

from apps.users.models import Profile


class ProfileSelector:
    def __init__(self, *, username: str) -> None:
        self.username = username

    def get_profile(self):
        profile = get_object_or_404(Profile, username=self.username)
        return profile
