from django.db import transaction
from apps.users.models import Profile, Follow


class SubscriptionService:
    model = Follow

    @transaction.atomic
    def follow(self, *, follower: Profile, following: Profile):
        follow = self.model(follower=follower, following=following)
        follow.full_clean()
        follow.save()
        follower.following_count += 1
        following.follower_count += 1
        follower.save()
        following.save()
        return follow

    @transaction.atomic
    def unfollow(self, *, subscription: Follow):
        subscription.delete()
        follower, following = subscription.follower, subscription.following
        follower.following_count -= 1
        following.follower_count -= 1
        follower.save()
        following.save()
