from django.db.models import QuerySet

from apps.blogs.filters import PostFilter
from apps.blogs.models import Post


def get_posts_list(*, filters: dict = None) -> QuerySet[Post]:
    filters = filters or {}
    posts = Post.objects.all()
    print(filters)
    return PostFilter(filters, posts).qs
