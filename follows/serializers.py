from rest_framework import serializers
from django.db import IntegrityError
from profiles.serializers import ProfileSerializer
from .models import Follow
from django.contrib.auth.models import User


class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer(source='follower.profile', read_only=True)
    following = ProfileSerializer(source='following.profile', read_only=True)
    follower_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='follower')
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='following')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following',
                  'follower_id', 'following_id', 'created_at']
        read_only_fields = ['follower', 'following', 'created_at']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('You already follow this user.')
