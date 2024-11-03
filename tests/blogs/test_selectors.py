import pytest

from apps.blogs.selectors.likes import get_post_likes
from apps.blogs.selectors.posts import get_posts_list, get_post_detail, get_subscription_posts_list
from apps.users.models import Profile


@pytest.mark.django_db
def test_get_posts_list(profile_factory, post_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    post_factory.create_batch(3, owner=profile)
    post_factory.create_batch(2, owner=another_profile)

    posts = get_posts_list()

    assert posts.count() == 5


@pytest.mark.django_db
def test_get_search_posts(profile_factory, post_factory):
    profile = profile_factory()
    post_factory.create_batch(3, owner=profile)
    post_factory(title="Test post")
    post_factory(content="This is a test post")
    filters = {"search": "test post"}
    posts = get_posts_list(filters=filters)

    assert posts.count() == 2


@pytest.mark.django_db
def test_get_post_detail(post_factory):
    post = post_factory()

    retrieved_post = get_post_detail(slug=post.slug, profile=post.owner)

    assert retrieved_post == post


@pytest.mark.django_db
def test_get_subscription_posts_list(profile_factory, follow_factory, post_factory):
    follower = profile_factory()
    followings = profile_factory.create_batch(3)
    for index, following in enumerate(followings):
        post_factory.create_batch(2, owner=following)
        if index == 1:
            continue
        follow_factory(follower=follower, following=following)

    subscriptions = Profile.objects.filter(follows__follower=follower)

    posts = get_subscription_posts_list(subscriptions=subscriptions)

    assert posts.count() == 4
    assert all(post.owner in subscriptions for post in posts)


@pytest.mark.django_db
def test_get_post_likes_no_likes(post_factory):
    likes = get_post_likes(post_factory())
    assert likes.count() == 0


@pytest.mark.django_db
def test_get_post_likes(post_factory, profile_factory, like_factory):
    profiles = profile_factory.create_batch(3)
    post = post_factory()
    for profile in profiles:
        like_factory(post=post, profile=profile)

    likes = get_post_likes(post)

    assert likes.count() == 3
    for profile in profiles:
        assert profile in likes
