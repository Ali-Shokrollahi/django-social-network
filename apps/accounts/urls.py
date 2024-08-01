from django.urls import path
from .apis import RegistrationAPIView

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
]
