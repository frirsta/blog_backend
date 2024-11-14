from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if not user.is_active:
            raise PermissionDenied("User account is disabled.")

        return user
