from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_picture = serializers.SerializerMethodField()
    cover_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        return obj.profile_picture.url if obj.profile_picture else 'https://res.cloudinary.com/ddms7cvqu/image/upload/v1/blog_media/profile_pictures/default.png'

    def get_cover_picture(self, obj):
        return obj.cover_picture.url if obj.cover_picture else 'https://res.cloudinary.com/ddms7cvqu/image/upload/v1/blog_media/cover_pictures/default.png'

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.user == request.user

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio',
                  'profile_picture', 'location', 'website', 'id', 'user', 'cover_picture', 'owner', 'is_owner']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError(
                "Username must be at least 3 characters long.")

        # Make the check case-insensitive
        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError("Username already exists.")

        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
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
