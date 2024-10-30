from django.urls import path

from .apis import PostApi, PostDetailApi, FeedApi

urlpatterns = [
    path("posts/", PostApi.as_view(), name="post_list"),
    path("post/<str:username>/<slug:slug>/", PostDetailApi.as_view(), name="post_detail"),

    path("posts/feed/", FeedApi.as_view(), name="feed")

]
