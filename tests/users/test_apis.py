import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_get_profile_not_found(api_client, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_detail', kwargs={'username': 'nonexistentuser'})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_profile_not_forbidden(api_client, profile):
    url = reverse('profile_detail', kwargs={'username': profile.username})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_put_profile_success(api_client, profile, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_detail', kwargs={'username': profile.username})
    data = {'first_name': 'new firstname', 'last_name': 'new lastname', 'bio': 'new bio'}
    response = api_client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'new firstname'
    assert response.data['last_name'] == 'new lastname'
    assert response.data['bio'] == 'new bio'


@pytest.mark.django_db
def test_put_profile_permission_denied(api_client, another_profile, user):
    api_client.force_authenticate(user=user)

    url = reverse('profile_detail', kwargs={'username': another_profile.username})
    data = {'first_name': 'unauthorized', 'bio': 'unauthorized bio'}
    response = api_client.put(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
