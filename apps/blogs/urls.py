from django.urls import path

from .apis import PostApi, PostDetailApi, FeedApi, PostUpdateDeleteApi, LikeCreateDeleteApi, PostLikeGetApi

urlpatterns = [
    path("posts/", PostApi.as_view(), name="post_list"),
    path("posts/<str:username>/<slug:slug>/", PostDetailApi.as_view(), name="post_detail"),
    path("posts/<slug:slug>/", PostUpdateDeleteApi.as_view(), name="post_update_delete"),

    path("posts/<str:username>/<slug:slug>/like/", LikeCreateDeleteApi.as_view(), name="post_create_delete"),
    path("posts/<str:username>/<slug:slug>/likes/", PostLikeGetApi.as_view(), name="post_likes"),

    path("posts/feed/", FeedApi.as_view(), name="feed")

]
