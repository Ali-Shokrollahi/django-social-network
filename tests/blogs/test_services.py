# from django.utils.text import slugify
# from apps.blogs.models import Post
# from apps.blogs.services.post import create_post
#
#
# def test_create_post(profile, post_data):
#     """Test creating a post with the create_post service function."""
#     post = create_post(title=post_data["title"], content=post_data["content"], owner=profile)
#
#     # Verify that the post is created successfully
#     assert post.title == post_data["title"]
#     assert post.content == post_data["content"]
#     assert post.owner == profile
#     assert post.slug == slugify(post_data["title"])
#
#     # Verify the post is in the database
#     assert Post.objects.filter(id=post.id).exists()
