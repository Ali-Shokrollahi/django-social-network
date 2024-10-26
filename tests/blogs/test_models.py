from django.db.utils import IntegrityError
import pytest

from apps.blogs.models import Post


def test_unique_constraint(profile, post_data):
    """Test unique constraint on owner and slug."""
    Post.objects.create(
        **post_data,
        owner=profile,
    )
    with pytest.raises(IntegrityError):
        # Attempt to create another post with the same owner and slug
        Post.objects.create(
            **post_data,
            owner=profile,
        )


def test_str_method(post):
    """Test the __str__ method of Post model."""
    assert str(post) == "test-slug"
