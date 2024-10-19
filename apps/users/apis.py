from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView

from .models import Profile, Follow
from .permissions import IsOwnerOrAuthenticatedReadOnly
from .selectors.profiles import ProfileSelector
from .selectors.subscription import SubscriptionSelector
from .services.profile import ProfileService
from .services.subscription import SubscriptionService


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


class ProfileUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class ProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ['first_name', 'last_name', 'bio']

    class ProfileInputSerializer(serializers.Serializer):
        bio = serializers.CharField(max_length=255, required=False)
        first_name = serializers.CharField(max_length=32, required=False)
        last_name = serializers.CharField(max_length=32, required=False)

    @extend_schema(request=ProfileInputSerializer, responses=ProfileOutputSerializer)
    def put(self, request):
        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = self.ProfileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ProfileService()
        new_profile = service.update_profile(profile=profile, **serializer.validated_data)
        return Response(self.ProfileOutputSerializer(new_profile).data, status=status.HTTP_200_OK)


class UsernameUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class UpdateUsernameInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32,
                                         validators=[UniqueValidator(queryset=Profile.objects.all())])

    @extend_schema(request=UpdateUsernameInputSerializer)
    def patch(self, request):
        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = self.UpdateUsernameInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = ProfileService()
        service.update_username(profile=profile, username=serializer.validated_data['username'])
        return Response(data="username updated successfully", status=status.HTTP_200_OK)


class SubscriptionCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class SubscriptionInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32)

    @staticmethod
    def _get_object(username: str) -> Profile:
        selector = ProfileSelector(username=username)
        return selector.get_profile()

    def post(self, request, username: str):
        serializer = self.SubscriptionInputSerializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        follower = request.user.profile
        following = self._get_object(username=serializer.validated_data['username'])
        try:
            SubscriptionService().follow(follower=follower, following=following)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)
        return Response("followed successfully", status=status.HTTP_201_CREATED)


class SubscriptionDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    class SubscriptionDeleteInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32)

    @staticmethod
    def _get_object(follower: Profile, following_username: str) -> Follow:
        following = ProfileSelector(username=following_username).get_profile()
        subscription = SubscriptionSelector.get_subscription(follower=follower, following=following)
        return subscription

    def delete(self, request, username: str):
        serializer = self.SubscriptionDeleteInputSerializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        follower = request.user.profile
        subscription = self._get_object(follower, following_username=serializer.validated_data['username'])
        SubscriptionService().unfollow(subscription=subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingGetApi(APIView):
    permission_classes = [IsAuthenticated]

    class FollowingGetInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32)

    class FollowingGetOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ["username", "first_name", "last_name"]

    @staticmethod
    def _get_object(username: str):
        return ProfileSelector(username=username).get_profile_following()

    def get(self, request, username: str):
        serializer = self.FollowingGetInputSerializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        followings = self._get_object(username=serializer.validated_data['username'])
        return Response(self.FollowingGetOutputSerializer(followings, many=True).data, status=status.HTTP_200_OK)


class FollowerGetApi(APIView):
    permission_classes = [IsAuthenticated]

    class FollowerGetInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=32)

    class FollowerGetOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ["username", "first_name", "last_name"]

    @staticmethod
    def _get_object(username: str):
        return ProfileSelector(username=username).get_profile_followers()

    def get(self, request, username: str):
        serializer = self.FollowerGetInputSerializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        followings = self._get_object(username=serializer.validated_data['username'])
        return Response(self.FollowerGetOutputSerializer(followings, many=True).data, status=status.HTTP_200_OK)
