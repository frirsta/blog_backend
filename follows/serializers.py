from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'
