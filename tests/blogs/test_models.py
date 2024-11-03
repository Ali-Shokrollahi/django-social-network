from django.db.utils import IntegrityError
import pytest

from apps.blogs.models import Post


@pytest.mark.django_db
def test_unique_constraint(profile_factory, post_data):
    """Test unique constraint on owner and slug."""
    profile = profile_factory()
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


@pytest.mark.django_db
def test_str_method(post_factory):
    """Test the __str__ method of Post model."""
    post = post_factory()
    assert str(post) == post.slug
