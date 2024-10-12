from django.shortcuts import get_object_or_404

from apps.users.models import Profile, Follow


class SubscriptionSelector:
    @staticmethod
    def get_subscription(*, follower: Profile, following: Profile) -> Follow:
        subscription = get_object_or_404(Follow, follower=follower, following=following)
        return subscription
