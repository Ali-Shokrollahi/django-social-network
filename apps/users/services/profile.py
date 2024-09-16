from apps.users.models import Profile


class ProfileService:
    model = Profile

    @staticmethod
    def update_profile(profile: Profile, first_name: str, last_name: str, bio: str) -> Profile:
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.full_clean()
        profile.save()
        return profile
