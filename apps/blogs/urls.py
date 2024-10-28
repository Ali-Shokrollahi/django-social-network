from django.urls import path

from .apis import PostApi

urlpatterns = [
    path("posts/", PostApi.as_view(), name="post_list"),

]
