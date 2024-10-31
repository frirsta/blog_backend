from rest_framework import serializers
from django.db import IntegrityError
from profiles.serializers import ProfileSerializer
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer(source='follower.profile', read_only=True)
    following = ProfileSerializer(source='following.profile', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('You already follow this user.')
