from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='author.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.author == request.user

    def get_profile_picture(self, obj):
        try:
            return obj.author.profile.profile_picture.url
        except AttributeError:
            return None

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'owner', 'is_owner',
                  'profile_picture', 'image', 'created_at', 'updated_at', 'author']
