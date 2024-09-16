from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .apis import RegistrationAPIView, EmailConfirmView, MyAccountView

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path('confirm-email/<str:token>/', EmailConfirmView.as_view(), name='email_confirm'),
    path('me/', MyAccountView.as_view(), name='me'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
