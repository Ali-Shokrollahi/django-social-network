from django.urls import path

from .apis import ProfileDetailApi, ProfileUpdateApi, UsernameUpdateApi, SubscriptionCreateApi, SubscriptionDeleteApi

urlpatterns = [
    path("<str:username>/", ProfileDetailApi.as_view(), name="profile_detail"),

    path("<str:username>/follow/", SubscriptionCreateApi.as_view(), name="follow"),
    path("<str:username>/unfollow/", SubscriptionDeleteApi.as_view(), name="unfollow"),

    path("dashboard/edit_profile/", ProfileUpdateApi.as_view(), name="profile_update"),
    path("dashboard/update_username/", UsernameUpdateApi.as_view(), name="username_update"),

]
