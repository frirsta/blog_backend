from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source='followers.count', read_only=True)
    following_count = serializers.IntegerField(
        source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count']
