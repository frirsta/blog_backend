from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework import serializers

class CurrentUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    cover_picture = serializers.ImageField(source='profile.cover_picture', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)
    website = serializers.URLField(source='profile.website', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'profile_picture', 'cover_picture',
            'bio', 'location', 'website', 'first_name', 'last_name',
        ]
