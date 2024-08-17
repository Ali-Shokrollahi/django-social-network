from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from .models import Profile
from .selectors.profiles import ProfileSelector


class ProfileDetailApi(APIView):
    class ProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['username', 'bio', 'post_count', 'follower_count', 'following_count']

    def get(self, request, username: str):
        selector = ProfileSelector(username=username)
        profile = selector.get_profile()
        return Response(self.ProfileOutputSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileUpdateApi(APIView):
    class ProfileInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32)
        bio = serializers.CharField(max_length=255, required=False)
        first_name = serializers.CharField(max_length=32, required=False)
        last_name = serializers.CharField(max_length=32, required=False)

