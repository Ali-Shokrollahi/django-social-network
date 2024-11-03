import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.blogs.models import Post
from apps.users.models import Profile


@pytest.mark.django_db
def test_create_post(authenticated_client, post_data):
    url = reverse("post_list")
    response = authenticated_client.post(url, data=post_data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_posts_list(authenticated_client, post_factory):
    post_factory.create_batch(3)
    url = reverse("post_list")
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_post_detail(authenticated_client, post_factory):
    post = post_factory()
    url = reverse("post_detail", args=[post.owner.username, post.slug])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == post.title
    assert response.data["content"] == post.content


@pytest.mark.django_db
def test_update_post(api_client, post_factory, profile_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    api_client.force_authenticate(user=profile.user)
    url = reverse("post_update_delete", args=[post.slug])
    update_data = {"title": "Updated title", "content": "Updated content"}
    response = api_client.patch(url, data=update_data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_post(api_client, post_factory, profile_factory):
    profile = profile_factory()
    post = post_factory(owner=profile)
    api_client.force_authenticate(user=profile.user)
    url = reverse("post_update_delete", args=[post.slug])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_feed_api(api_client, profile_factory, post_factory, follow_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    api_client.force_authenticate(profile.user)
    follow_factory(follower=profile, following=another_profile)
    post_factory.create_batch(3, owner=another_profile)

    url = reverse("feed")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_post_likes(authenticated_client, post_factory, profile_factory, like_factory):
    post = post_factory()
    like_factory.create_batch(3, post=post)

    url = reverse('post_likes', kwargs={'username': post.owner.username, 'slug': post.slug})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_like_post(authenticated_client, post_factory, profile_factory):
    post = post_factory()

    url = reverse('like_create_delete', kwargs={'username': post.owner.username, 'slug': post.slug})
    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == "Post liked successfully."


@pytest.mark.django_db
def test_unlike_post(api_client, post_factory, profile_factory, like_factory):
    post = post_factory()
    profile = profile_factory()
    like_factory(post=post, profile=profile)
    api_client.force_authenticate(user=profile.user)

    url = reverse('like_create_delete', kwargs={'username': post.owner.username, 'slug': post.slug})
    response = api_client.delete(url)

    # Verify the response and that the like was deleted
    assert response.status_code == status.HTTP_204_NO_CONTENT
