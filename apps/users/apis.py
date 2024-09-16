from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .permissions import IsOwnerOrAuthenticatedReadOnly
from .selectors.profiles import ProfileSelector
from .services.profile import ProfileService


class ProfileDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAuthenticatedReadOnly]

    class ProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['username', 'first_name', 'last_name', 'bio', 'post_count', 'follower_count', 'following_count']

    class ProfileInputSerializer(serializers.Serializer):
        bio = serializers.CharField(max_length=255, required=False)
        first_name = serializers.CharField(max_length=32, required=False)
        last_name = serializers.CharField(max_length=32, required=False)

    @staticmethod
    def _get_object(username: str) -> Profile:
        selector = ProfileSelector(username=username)
        return selector.get_profile()

    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request, username: str):
        profile = self._get_object(username=username)
        return Response(self.ProfileOutputSerializer(profile).data, status=status.HTTP_200_OK)

    @extend_schema(request=ProfileInputSerializer, responses=ProfileOutputSerializer)
    def put(self, request, username: str):
        serializer = self.ProfileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self._get_object(username=username)
        self.check_object_permissions(request, profile)
        service = ProfileService()
        new_profile = service.update_profile(profile=profile, **serializer.validated_data)
        return Response(self.ProfileOutputSerializer(new_profile).data, status=status.HTTP_200_OK)
