import pytest
from django.urls import reverse
from rest_framework import status

from apps.accounts.services.registration import EmailConfirmationToken
from apps.users.models import Profile


@pytest.mark.django_db
def test_registration_success(api_client, user_data, django_user_model):
    url = reverse('register')
    user_data['confirm_password'] = user_data['password']
    response = api_client.post(url, user_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data
    assert django_user_model.objects.filter(email=user_data['email']).exists()
    assert Profile.objects.filter(username=user_data['username']).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "password, confirm_password, expected_status, expected_error_code",
    [
        ("Password123", "Password123", status.HTTP_400_BAD_REQUEST,
         "password_must_include_special_char"),  # No special char
        ("12345678!", "12345678!", status.HTTP_400_BAD_REQUEST, "password_must_include_letter"),
        # No letter
        ("Password!", "Password!", status.HTTP_400_BAD_REQUEST, "password_must_include_number"),
        # No number

    ]
)
def test_password_validation(api_client, password, confirm_password, expected_status, expected_error_code):
    user_data = {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': password,
        'confirm_password': confirm_password
    }
    url = reverse('register')
    response = api_client.post(url, user_data, format='json')

    assert response.status_code == expected_status

    assert response.data['password'][0].code == expected_error_code


@pytest.mark.django_db
def test_password_match(api_client):
    user_data = {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'Password123!',
        'confirm_password': 'DifferentPassword123!'
    }
    url = reverse('register')
    response = api_client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0].code == 'password_must_match'


@pytest.mark.django_db
def test_email_confirmation_success(api_client, user_data, user1):
    token = EmailConfirmationToken.for_user(user1)
    email_confirm_url = reverse('email_confirm', args=[str(token)])

    response = api_client.get(email_confirm_url)

    assert response.status_code == status.HTTP_200_OK
    user1.refresh_from_db()
    assert user1.is_active
    assert user1.is_verified


@pytest.mark.django_db
def test_email_confirmation_invalid_token(api_client):
    invalid_token = "invalidtoken123"
    email_confirm_url = reverse('email_confirm', args=[invalid_token])

    response = api_client.get(email_confirm_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Token is invalid or expired' in response.data['data']
