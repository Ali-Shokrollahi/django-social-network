import pytest
from django.urls import reverse
from rest_framework import status


def test_get_profile_success(api_client, profile, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_detail', kwargs={'username': profile.username})
    response = api_client.get(url)

    # Assert status and profile data
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == profile.username
    assert response.data['first_name'] == profile.first_name
    assert response.data['last_name'] == profile.last_name
    assert response.data['bio'] == profile.bio


def test_get_profile_not_found(api_client, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_detail', kwargs={'username': 'nonexistentuser'})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_profile_unauthorized(api_client, profile):
    url = reverse('profile_detail', kwargs={'username': profile.username})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_put_profile_success(api_client, profile, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_update')
    data = {'first_name': 'new firstname', 'last_name': 'new lastname', 'bio': 'new bio'}
    response = api_client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'new firstname'
    assert response.data['last_name'] == 'new lastname'
    assert response.data['bio'] == 'new bio'


def test_patch_username_success(api_client, profile, user):
    api_client.force_authenticate(user=user)
    url = reverse('username_update')
    response = api_client.patch(url, {'username': 'new username'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == 'username updated successfully'


def test_create_subscription_success(api_client, profile, another_profile):
    api_client.force_authenticate(user=profile.user)
    url = reverse('follow', kwargs={'username': another_profile.username})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == "followed successfully"


def test_subscription_create_user_not_found(api_client, profile):
    api_client.force_authenticate(user=profile.user)
    url = reverse('follow', kwargs={'username': "notexists"})
    response = api_client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_subscription_delete_success(api_client, follow_relationship):
    api_client.force_authenticate(user=follow_relationship.follower.user)
    url = reverse('unfollow', kwargs={'username': follow_relationship.following.username})

    # Perform the delete request to unfollow a user
    response = api_client.delete(url)

    # Assert that the unfollow action was successful
    assert response.status_code == status.HTTP_204_NO_CONTENT
