from django.db.models import QuerySet

from apps.blogs.models import Post
from apps.users.models import Profile


def get_post_likes(post: Post) -> QuerySet[Profile]:
    profiles = Profile.objects.filter(likes__post=post)
    return profiles
