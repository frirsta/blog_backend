from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers
from follows.models import Follow
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    following_count = serializers.ReadOnlyField()
    posts_count = serializers.ReadOnlyField()
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    cover_picture = serializers.ImageField(allow_null=True, required=False)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_is_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(follower=user, following=obj.user).exists()
        return False

    def get_followers(self, obj):
        followers = Follow.objects.filter(
            following=obj.user)  # Users who follow this user
        return [{'id': follow.follower.id, 'username': follow.follower.username} for follow in followers]

    def get_following(self, obj):
        following = Follow.objects.filter(
            follower=obj.user)  # Users this user is following
        return [{'id': follow.following.id, 'username': follow.following.username} for follow in following]

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj.user).count()

    def get_following_id(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            follow_relation = Follow.objects.filter(
                follower=user, following=obj.user).first()
            return follow_relation.id if follow_relation else None
        return None

    def validate_website(self, value):
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'bio', 'profile_picture', 'cover_picture',
            'location', 'website', 'id', 'user', 'is_owner', 'is_following',
            'following_id', 'following_count', 'followers_count', 'posts_count', 'created_at', 'updated_at', 'followers', 'following'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError("Username already exists.")

        return value.lower()

    def validate_email(self, value):
        # Ensure email is unique case-insensitively
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['username'].lower()

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user)

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
