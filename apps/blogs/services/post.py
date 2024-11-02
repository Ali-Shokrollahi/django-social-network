from django.db import transaction
from django.utils.text import slugify

from apps.users.models import Profile
from apps.blogs.models import Post


@transaction.atomic
def create_post(*, title: str, content: str, owner: Profile) -> Post:
    post = Post.objects.create(slug=slugify(title), title=title, content=content, owner=owner)
    owner.post_count += 1
    owner.save()
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


@transaction.atomic
def delete_post(*, post: Post) -> None:
    post.delete()
    post.owner.post_count -= 1
    post.owner.save()
