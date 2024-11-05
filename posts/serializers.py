from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='author.username')
    is_owner = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    likes_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'owner', 'is_owner',
            'profile_picture', 'image', 'created_at', 'updated_at', 'likes_id', 'likes_count'
        ]
        read_only_fields = ['owner', 'is_owner',
                            'profile_picture', 'created_at', 'updated_at']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.author == request.user

    def get_profile_picture(self, obj):
        try:
            return obj.author.profile.profile_picture.url
        except AttributeError:
            return None

    def get_likes_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            likes = Like.objects.filter(user=user, post=obj).first()
            return likes.id if likes else None
        return None

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value
