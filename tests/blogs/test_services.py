import pytest
from django.utils.text import slugify
from apps.blogs.models import Post, Like
from apps.blogs.services.likes import create_like, delete_like
from apps.blogs.services.posts import create_post, update_post, delete_post


@pytest.mark.django_db
def test_create_post(profile_factory, post_data):
    """Test creating a post with the create_post service function."""

    profile = profile_factory()
    post = create_post(title=post_data["title"], content=post_data["content"], owner=profile)

    # Verify that the post is created successfully
    assert post.title == post_data["title"]
    assert post.content == post_data["content"]
    assert post.owner == profile
    assert post.slug == slugify(post_data["title"])

    # Verify the post is in the database
    assert Post.objects.filter(id=post.id).exists()


@pytest.mark.django_db
def test_update_post_title(post_factory):
    post = post_factory()
    updated_title = "Updated Title"

    updated_post = update_post(post=post, title=updated_title)

    assert updated_post.title == updated_title
    assert updated_post.slug == "updated-title"
    assert updated_post.content == post.content


@pytest.mark.django_db
def test_update_post_content(post_factory):
    post = post_factory()
    updated_content = " This is updated content"

    updated_post = update_post(post=post, content=updated_content)

    assert updated_post.title == post.title
    assert updated_post.slug == post.slug
    assert updated_post.content == updated_content


@pytest.mark.django_db
def test_delete_post(post_factory, profile_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)

    delete_post(post=post)

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    profile.refresh_from_db()
    assert profile.post_count == 0


@pytest.mark.django_db
def test_create_like(post_factory, profile_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    create_like(post=post, profile=profile)

    assert Like.objects.filter(post=post, profile=profile).exists()


@pytest.mark.django_db
def test_create_like_already_exists(post_factory, profile_factory, like_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    like_factory(post=post, profile=profile)

    # Call the service again, which should not create a duplicate
    create_like(post=post, profile=profile)

    # Ensure only one Like object exists
    assert Like.objects.filter(post=post, profile=profile).count() == 1


@pytest.mark.django_db
def test_delete_like(post_factory, profile_factory, like_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    like_factory(post=post, profile=profile)

    delete_like(post=post, profile=profile)

    assert not Like.objects.filter(post=post, profile=profile).exists()


@pytest.mark.django_db
def test_delete_like_not_exists(post_factory, profile_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    assert not Like.objects.filter(post=post, profile=profile).exists()

    delete_like(post=post, profile=profile)

    assert not Like.objects.filter(post=post, profile=profile).exists()
