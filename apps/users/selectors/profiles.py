from django.shortcuts import get_object_or_404

from apps.users.models import Profile


class ProfileSelector:
    def __init__(self, *, username: str) -> None:
        self.username = username

    def get_profile(self):
        profile = get_object_or_404(Profile, username=self.username)
        return profile

    def get_profile_followers(self):
        profile = self.get_profile()
        return Profile.objects.filter(followed_by__following=profile)

    def get_profile_following(self):
        profile = self.get_profile()
        return Profile.objects.filter(follows__follower=profile)
