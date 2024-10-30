from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.blogs.filters import PostFilter
from apps.blogs.models import Post
from apps.users.models import Profile


def get_posts_list(*, filters: dict = None) -> QuerySet[Post]:
    filters = filters or {}
    posts = Post.objects.all()
    return PostFilter(filters, posts).qs


def get_post_detail(*, slug: str, profile: Profile) -> Post:
    return get_object_or_404(profile.posts, slug=slug)


def get_subscription_posts_list(*, subscriptions: QuerySet[Profile]) -> QuerySet[Post]:
    posts = Post.objects.filter(owner__in=subscriptions).order_by("-updated_at")
    return posts
