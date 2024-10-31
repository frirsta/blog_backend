from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    cover_picture = serializers.ImageField(allow_null=True, required=False)

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.user == request.user
        return False

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if request.user.is_authenticated:
                return obj.user.followers.filter(follower=request.user).exists()
        return False

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
            'location', 'website', 'id', 'user', 'owner', 'is_owner', 'is_following'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError(
                "Username must be at least 3 characters long.")

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
