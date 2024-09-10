from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.models import Profile
from .services.registration import RegistrationService
from .validators import number_validator, letter_validator, special_char_validator

User = get_user_model()


class RegistrationAPIView(APIView):
    class RegistrationInputSerializer(serializers.Serializer):
        email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
        username = serializers.CharField(max_length=32,
                                         validators=[UniqueValidator(queryset=Profile.objects.all())])
        password = serializers.CharField(max_length=254, min_length=8,
                                         validators=[number_validator, letter_validator, special_char_validator])
        confirm_password = serializers.CharField(max_length=254)

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError(code='password_must_match', detail='Passwords must match')

            return attrs

    class RegistrationOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('email', 'created_at')

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['token'] = self.context['token']
            return representation

    @extend_schema(request=RegistrationInputSerializer, responses=RegistrationOutputSerializer)
    def post(self, request):
        serializer = self.RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = RegistrationService()
        user, token = service.register(email=serializer.validated_data['email'],
                                       username=serializer.validated_data['username'],
                                       password=serializer.validated_data['password'], )

        return Response(self.RegistrationOutputSerializer(user, context={'token': token}).data,
                        status=status.HTTP_201_CREATED)


class EmailConfirmView(APIView):
    def get(self, request, token):
        try:
            service = RegistrationService()
            service.activate_user(token=token)
        except TokenError as e:
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Email confirmed successfully'}, status=status.HTTP_200_OK)
