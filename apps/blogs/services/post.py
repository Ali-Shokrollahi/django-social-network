from django.utils.text import slugify

from apps.users.models import Profile
from apps.blogs.models import Post


def create_post(*, title: str, content: str, owner: Profile) -> Post:
    post = Post.objects.create(slug=slugify(title), title=title, content=content, owner=owner)
    return post


def update_post(*, post: Post, title: str | None, content: str | None) -> Post:
    if title is not None:
        post.title = title
        post.slug = slugify(title)
    if content is not None:
        post.content = content
    post.full_clean()
    post.save()
    return post


def delete_post(*, post: Post) -> None:
    post.delete()
