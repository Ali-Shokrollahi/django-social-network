from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
from django.urls import reverse
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, Token

from ..exceptions import UserAlreadyActivatedException
from apps.users.models import Profile


class EmailConfirmationToken(Token):
    lifetime = timedelta(hours=1)
    token_type = 'email_confirmation'


class RegistrationService:
    User = get_user_model()

    @transaction.atomic
    def register(self, *, email: str, username: str, password: str) -> tuple[User, dict]:
        user = self._create_user(email=email, password=password)
        self._create_profile(user=user, username=username)
        self._send_confirmation_email(user=user)
        user_token = self._get_token(user=user)
        return user, user_token

    def _create_user(self, *, email: str, password: str) -> User:
        return self.User.objects.create_user(email=email, password=password)
        # return self.User(email=email, password=password)

    @staticmethod
    def _create_profile(*, user: User, username: str) -> None:
        Profile.objects.create(user=user, username=username)

    @staticmethod
    def _get_token(*, user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    @staticmethod
    def _send_confirmation_email(*, user: User) -> None:
        token = EmailConfirmationToken.for_user(user)
        confirmation_url = f"{settings.SITE_URL}{reverse('email_confirm', args=[token])}"

        message = EmailMessage('email_confirmation.html', {'user': user, 'activation_url': confirmation_url},
                               from_email=settings.FROM_EMAIL,
                               to=[user.email])
        message.send()

    def activate_user(self, *, token) -> None:
        email_token = EmailConfirmationToken(token=token)
        user_id = email_token.payload.get('user_id')
        user = self.User.objects.get(id=user_id)
        if user.is_verified:
            raise UserAlreadyActivatedException()
        user.is_active = True
        user.is_verified = True
        user.save()
