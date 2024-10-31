from django.db import IntegrityError
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.pagination import LimitOffsetPagination, get_paginated_response_context
from apps.blogs.models import Post
from apps.blogs.selectors.posts import get_posts_list, get_post_detail, get_subscription_posts_list
from apps.blogs.services.post import create_post, update_post, delete_post
from apps.users.selectors.profiles import ProfileSelector


class PostApi(APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class FilterSerializer(serializers.Serializer):
        search = serializers.CharField(required=False, max_length=100)
        updated_at_after = serializers.CharField(required=False, max_length=10)
        updated_at_before = serializers.CharField(required=False, max_length=10)

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=64)
        content = serializers.CharField(max_length=512)

    class PostOutputSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField("_get_post_url")
        owner = serializers.SerializerMethodField("_get_post_owner")
        summary = serializers.SerializerMethodField("_get_post_summary")

        class Meta:
            model = Post
            fields = ["id", "title", "summary", "owner", "updated_at", "url"]

        def _get_post_url(self, post):
            request = self.context.get("request")
            path = reverse("post_detail", args=(post.owner.username, post.slug,))
            return request.build_absolute_uri(path)

        @staticmethod
        def _get_post_owner(post):
            return post.owner.username

        @staticmethod
        def _get_post_summary(post):
            return post.content[:47] + "..."

    @extend_schema(request=PostInputSerializer, responses=PostOutputSerializer)
    def post(self, request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            post = create_post(title=serializer.validated_data["title"],
                               content=serializer.validated_data["content"],
                               owner=request.user.profile
                               )
        except IntegrityError:
            return Response(data="There is a post with this owner and title", status=status.HTTP_400_BAD_REQUEST)

        return Response(self.PostOutputSerializer(post, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[FilterSerializer], responses=PostOutputSerializer)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        posts = get_posts_list(filters=filters_serializer.validated_data)
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.PostOutputSerializer,
            queryset=posts,
            request=request,
            view=self,
        )


class PostDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    class PostDetailOutputSerializer(serializers.ModelSerializer):
        owner = serializers.SerializerMethodField("_get_post_owner")

        class Meta:
            model = Post
            fields = ["id", "title", "content", "owner", "updated_at"]

        @staticmethod
        def _get_post_owner(post):
            return post.owner.username

    @staticmethod
    def _get_object(username, slug):
        profile = ProfileSelector(username=username).get_profile()
        post = get_post_detail(slug=slug, profile=profile)
        return post

    @extend_schema(responses=PostDetailOutputSerializer)
    def get(self, request, username, slug):
        post = self._get_object(slug=slug, username=username)
        return Response(self.PostDetailOutputSerializer(post).data, status=status.HTTP_200_OK)


class PostUpdateDeleteApi(APIView):
    class PostUpdateInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=64, required=False)
        content = serializers.CharField(max_length=512, required=False)

    class PostUpdateOutputSerializer(serializers.ModelSerializer):
        owner = serializers.SerializerMethodField("_get_post_owner")

        class Meta:
            model = Post
            fields = ["id", "title", "content", "owner", "updated_at"]

        @staticmethod
        def _get_post_owner(post):
            return post.owner.username

    @staticmethod
    def _get_object(username, slug):
        profile = ProfileSelector(username=username).get_profile()
        post = get_post_detail(slug=slug, profile=profile)
        return post

    @extend_schema(request=PostUpdateInputSerializer, responses=PostUpdateOutputSerializer)
    def patch(self, request, slug):
        serializer = self.PostUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self._get_object(slug=slug, username=request.user.profile.username)

        try:
            post = update_post(post=post,
                               title=serializer.validated_data.get("title"),
                               content=serializer.validated_data.get("content"),
                               )
        except IntegrityError:
            return Response(data="There is a post with this owner and title", status=status.HTTP_400_BAD_REQUEST)

        return Response(self.PostUpdateOutputSerializer(post).data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        post = self._get_object(slug=slug, username=request.user.profile.username)
        delete_post(post=post)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedApi(APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class FeedOutputSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField("_get_post_url")
        owner = serializers.SerializerMethodField("_get_post_owner")
        summary = serializers.SerializerMethodField("_get_post_summary")

        class Meta:
            model = Post
            fields = ["id", "title", "summary", "owner", "updated_at", "url"]

        def _get_post_url(self, post):
            request = self.context.get("request")
            path = reverse("post_detail", args=(post.owner.username, post.slug,))
            return request.build_absolute_uri(path)

        @staticmethod
        def _get_post_owner(post):
            return post.owner.username

        @staticmethod
        def _get_post_summary(post):
            return post.content[:47] + "..."

    @staticmethod
    def _get_profile_subscriptions(request):
        subscriptions = ProfileSelector(username=request.user.profile.username).get_profile_following()
        return subscriptions

    def get(self, request):
        posts = get_subscription_posts_list(subscriptions=self._get_profile_subscriptions(request))
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.FeedOutputSerializer,
            queryset=posts,
            request=request,
            view=self,
        )
