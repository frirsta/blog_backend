from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            username = username.lower()  # Convert username to lowercase
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
