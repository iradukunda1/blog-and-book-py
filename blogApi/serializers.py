from rest_framework import serializers
from knox.models import AuthToken
from . import models


class HelloSerializer(serializers.Serializer):

    def create(self, validated_data):
        name = serializers.CharField(required=None)
        return name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = models.UserProfile(
            email=validated_data['email'],
            username=validated_data['username'],
            is_active=validated_data['is_active'],
            is_staff=validated_data['is_staff'],
        )
        user.set_password(validated_data['password'])

        user.save()

        return user


class ProfileFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfileFeedItem
        fields = '__all__'
        extra_kwargs = {"user_profile": {"read_only": True}}
