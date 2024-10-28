from django.urls import path, include


# v1 = [
#
# ]

urlpatterns = [
    path("accounts/", include("apps.accounts.urls"), name="accounts"),
    path("users/", include("apps.users.urls"), name="users"),
    path("blogs/", include("apps.blogs.urls"), name="blogs"),
]
