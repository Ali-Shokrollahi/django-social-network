from django.utils.text import slugify

from apps.users.models import Profile
from apps.blogs.models import Post


def create_post(*, title: str, content: str, owner: Profile):
    post = Post.objects.create(slug=slugify(title), title=title, content=content, owner=owner)
    return post
