from django.db import transaction
from django.contrib.auth import get_user_model

from apps.users.models import Profile


class RegistrationService:
    User = get_user_model()

    @transaction.atomic
    def register(self, *, email: str, username: str, password: str) -> User:
        user = self._create_user(email=email, password=password)
        self._create_profile(user=user, username=username)
        return user

    def _create_user(self, *, email: str, password: str) -> User:
        return self.User.objects.create_user(email=email, password=password)

    @staticmethod
    def _create_profile(*, user: User, username: str) -> None:
        Profile.objects.create(user=user, username=username)

    # @staticmethod
    # def _send_confirmation_email(*, user: User) -> None:
    #     subject = 'Confirm your email'
    #     from_email = '<EMAIL>'
    #     recipient_list = [user.email]

