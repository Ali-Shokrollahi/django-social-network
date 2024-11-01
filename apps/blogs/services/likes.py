from apps.blogs.models import Post, Like
from apps.users.models import Profile


def create_like(*, post: Post, profile: Profile) -> None:
    Like.objects.get_or_create(profile=profile, post=post)


def delete_like(*, post: Post, profile: Profile) -> None:
    like = Like.objects.filter(profile=profile, post=post).first()
    if like:
        like.delete()
