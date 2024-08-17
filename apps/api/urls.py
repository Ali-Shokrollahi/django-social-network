from django.urls import path, include


# v1 = [
#
# ]

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("users/", include("apps.users.urls")),
]
