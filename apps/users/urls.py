from django.urls import path

from .apis import ProfileDetailApi, ProfileUpdateApi, UsernameUpdateApi

urlpatterns = [
    path("<str:username>/", ProfileDetailApi.as_view(), name="profile_detail"),

    path("dashboard/edit_profile/", ProfileUpdateApi.as_view(), name="profile_update"),
    path("dashboard/update_username/", UsernameUpdateApi.as_view(), name="username_update"),

]
