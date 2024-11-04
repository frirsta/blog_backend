from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Profile

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def get_profile(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            return {
                'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                'cover_picture': profile.cover_picture.url if profile.cover_picture else None,
                'bio': profile.bio,
                'location': profile.location,
                'website': profile.website,
                'followers_count': profile.followers.count(),
                'following_count': profile.following.count()
            }
        except Profile.DoesNotExist:
            return None
