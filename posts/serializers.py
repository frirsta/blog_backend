from rest_framework import serializers
from .models import Post, Tag, Category
from likes.models import Like


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    owner_id = serializers.ReadOnlyField(source='user.id')
    is_owner = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    likes_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    category = CategorySerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, source='category')
    tags = TagSerializer(many=True, read_only=True)
    tags_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'user', 'owner_id', 'is_owner',
            'profile_picture', 'image', 'created_at', 'updated_at', 'likes_id', 'likes_count', 'comments_count', 'category_id', 'category', 'tags_names', 'tags'
        ]
        read_only_fields = ['user', 'is_owner', 'owner_id',
                            'profile_picture', 'created_at', 'updated_at']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.user == request.user

    def get_owner_id(self, obj):
        return obj.user.id

    def get_profile_picture(self, obj):
        try:
            return obj.user.profile.profile_picture.url
        except AttributeError:
            return None

    def get_likes_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            likes = Like.objects.filter(user=user, post=obj).first()
            return likes.id if likes else None
        return None

    def get_image(self, obj):
        if obj.image:
            image_url = obj.image.url
            if image_url.startswith("image/upload/"):
                return image_url.replace("image/upload/", "")
            return image_url
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

    def create(self, validated_data):
        tags_data = validated_data.pop('tags_names', [])
        post = super().create(validated_data)

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags_names', None)
        instance = super().update(instance, validated_data)

        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
