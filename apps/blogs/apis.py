from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blogs.models import Post
from apps.blogs.selectors.posts import get_posts_list
from apps.blogs.services.post import create_post


class PostApi(APIView):
    permission_classes = [IsAuthenticated]

    class FilterSerializer(serializers.Serializer):
        search = serializers.CharField(required=False, max_length=100)
        updated_at_after = serializers.CharField(required=False, max_length=10)
        updated_at_before = serializers.CharField(required=False, max_length=10)

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=64)
        content = serializers.CharField(max_length=512)

    class PostOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ["id", "title", "content", "owner", "created_at", "updated_at"]

    @extend_schema(request=PostInputSerializer, responses=PostOutputSerializer)
    def post(self, request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            post = create_post(title=serializer.validated_data["title"],
                               content=serializer.validated_data["content"],
                               owner=request.user.profile
                               )
        except IntegrityError as e:
            return Response(data="There is a post with this owner and title", status=status.HTTP_400_BAD_REQUEST)

        return Response(self.PostOutputSerializer(post).data, status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[FilterSerializer], responses=PostOutputSerializer)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        posts = get_posts_list(filters=filters_serializer.validated_data)
        return Response(self.PostOutputSerializer(posts, many=True).data, status=status.HTTP_200_OK)
