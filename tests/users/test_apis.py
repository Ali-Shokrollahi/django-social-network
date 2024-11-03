import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_profile_success(authenticated_client, profile_factory):
    profile = profile_factory()

    url = reverse('profile_detail', kwargs={'username': profile.username})
    response = authenticated_client.get(url)

    # Assert status and profile data
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == profile.username
    assert response.data['first_name'] == profile.first_name
    assert response.data['last_name'] == profile.last_name
    assert response.data['bio'] == profile.bio


@pytest.mark.django_db
def test_get_profile_not_found(authenticated_client):
    url = reverse('profile_detail', kwargs={'username': 'nonexistentuser'})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_profile_unauthorized(api_client, profile_factory):
    profile = profile_factory()
    url = reverse('profile_detail', kwargs={'username': profile.username})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_put_profile_success(authenticated_client):
    url = reverse('profile_update')
    data = {'first_name': 'new firstname', 'last_name': 'new lastname', 'bio': 'new bio'}
    response = authenticated_client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'new firstname'
    assert response.data['last_name'] == 'new lastname'
    assert response.data['bio'] == 'new bio'


@pytest.mark.django_db
def test_patch_username_success(authenticated_client):
    url = reverse('username_update')
    response = authenticated_client.patch(url, {'username': 'new username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == 'username updated successfully'


@pytest.mark.django_db
def test_create_subscription_success(authenticated_client, profile_factory):
    another_profile = profile_factory()
    url = reverse('follow', kwargs={'username': another_profile.username})
    response = authenticated_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == "followed successfully"


@pytest.mark.django_db
def test_subscription_create_user_not_found(authenticated_client):
    url = reverse('follow', kwargs={'username': "notexists"})
    response = authenticated_client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_subscription_delete_success(api_client, profile_factory, follow_factory):
    profile = profile_factory()
    another_profile = profile_factory()
    follow_relationship = follow_factory(follower=profile, following=another_profile)
    api_client.force_authenticate(user=follow_relationship.follower.user)
    url = reverse('unfollow', kwargs={'username': follow_relationship.following.username})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
