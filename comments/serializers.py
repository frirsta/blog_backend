from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    profile_picture = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_profile_picture(self, obj):
        return obj.user.profile.profile_picture.url

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'profile_id', 'profile_picture', 'post',
            'content', 'is_owner', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'profile_id',
                            'profile_picture', 'created_at', 'updated_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
