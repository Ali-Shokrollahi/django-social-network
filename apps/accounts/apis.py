from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

from apps.users.models import Profile
from .validators import number_validator, letter_validator, special_char_validator
from .services.registration import RegistrationService

User = get_user_model()


class RegistrationAPIView(APIView):
    class InputSerializer(serializers.Serializer):
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
                raise serializers.ValidationError('Passwords must match')

            return attrs

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('email', 'created_at')

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = RegistrationService()
        user = service.register(email=serializer.validated_data['email'],
                                username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'], )

        return Response(self.OutputSerializer(user).data)
