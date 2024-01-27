from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user import models
from user.utils import get_tokens


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=10, label='confirm password', write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(max_length=10, label='password', write_only=True, required=True)

    class Meta:
        model = models.User
        fields = [
                  'id',
                  'username',
                  'password',
                  'password2',
                  'first_name',
                  'last_name',
                  'token',
                  'role',
                 ]


    def validate(self, data):
        """
        Check that start is before finish.
        """
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise ValidationError('password must match')
        return data


    def create(self, validated_data):
        user = models.User.objects.create(
                                username=validated_data['username'],
                                password=validated_data['password'],
                                first_name=validated_data['first_name'],
                                last_name=validated_data['last_name'],
                                role=validated_data['role'],
                                          )
        return user


    def get_token(self, obj):
        user = models.User.objects.get(id=obj.id)
        token = get_tokens(user)
        refresh = token['refresh']
        access = token['access']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        return {
            "refresh": refresh,
            "access": access
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True, write_only=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                return data
            raise ValidationError('username or password is wrong')
        except:
            raise ValidationError('username or password is wrong')

    def get_user(self, obj):
        try:
            user = models.User.objects.get(username=obj['username'])
            user = UserSerializer(instance=user)
            return user.data
        except:
            raise ValidationError('username or password is wrong')

    def get_token(self, obj):
        user = models.User.objects.get(username=obj['username'])
        token = get_tokens(user)
        refresh = token['refresh']
        access = token['access']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        return {
            "refresh": refresh,
            "access": access
        }



class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=1000, required=True)

    def validate_refresh(self, data):
        if settings.REDIS_JWT_TOKEN.get(name=data):
            settings.REDIS_JWT_TOKEN.delete(data)
            return data
        else:
            raise ValidationError('token is invalid or expired')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=1000, required=True, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def validate_refresh(self, data):
        if settings.REDIS_JWT_TOKEN.get(name=data):
            return data
        else:
            raise ValidationError('Token is invalid or expired')


    def get_token(self, obj):
        refresh = settings.REDIS_JWT_TOKEN.get(name=obj['refresh'])
        token_refresh = RefreshToken(refresh)
        user = models.User.objects.get(id=token_refresh['user_id'])
        settings.REDIS_JWT_TOKEN.delete(refresh)
        token = get_tokens(user)
        access = token['access']
        refresh = token['refresh']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        data = {'access': access, 'refresh': refresh}
        return data