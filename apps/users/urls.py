from django.urls import path
from .apis import ProfileDetailApi

urlpatterns = [
    path("<str:username>/", ProfileDetailApi.as_view(), name="profile_detail"),
]
