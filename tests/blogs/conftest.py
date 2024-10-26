import pytest

from apps.blogs.models import Post


@pytest.fixture
def post_data():
    return {
        "slug": "test-slug",
        "title": "Test Title",
        "content": "This is test content.",

    }


@pytest.fixture
def post(profile, post_data):
    """Fixture to create a Post instance."""
    return Post.objects.create(**post_data, owner=profile)
