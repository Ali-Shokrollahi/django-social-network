import pytest


def test_create_user(django_user_model, user_data):
    user = django_user_model.objects.create_user(email=user_data['email'], password=user_data['password'])
    assert user.email == "testuser@email.com"
    assert user.is_active is False
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_verified is False
    assert str(user) == "testuser@email.com"
    assert user.has_usable_password()
    assert user.check_password("Test@1pass")


def test_create_superuser(django_user_model, user_data):
    user = django_user_model.objects.create_superuser(email=user_data['email'], password=user_data['password'])
    assert user.email == "testuser@email.com"
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_verified is True
    assert str(user) == "testuser@email.com"


def test_create_user_without_email(django_user_model):
    with pytest.raises(ValueError) as exc_info:
        django_user_model.objects.create_user(email=None)

    assert str(exc_info.value) == "Users must have an email address"


def test_create_user_with_unusable_password(django_user_model, user_data):
    user = django_user_model.objects.create_user(email=user_data['email'])
    assert not user.has_usable_password()
