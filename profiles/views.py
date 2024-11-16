from rest_framework import generics, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from blog.permissions import IsAuthorOrReadOnly
from .serializers import ProfileSerializer, UserRegistrationSerializer, PasswordResetSerializer
from .models import Profile


class UserRegistrationView(generics.CreateAPIView):
    """
    API view to register a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('user__posts', distinct=True),
        following_count=Count('user__following', distinct=True),
        followers_count=Count('user__followers', distinct=True),
    ).order_by('created_at')

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this profile.")
        user = instance.user
        user.delete()
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_200_OK)


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('user__posts', distinct=True),
        following_count=Count('user__following', distinct=True),
        followers_count=Count('user__followers', distinct=True),
    ).order_by('created_at')
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username']
    ordering_fields = ['created_at', 'posts_count',
                       'following_count', 'followers_count']
    filterset_fields = [
        'user__following__following',  # Users they are following
        'user__followers__follower',  # Users that follow them
    ]


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"https://frirsta-blog-frontend-bfdde69332c7.herokuapp.com/password-reset-confirm/{
                uid}/{token}/"

            context = {
                'username': user.username,
                'reset_url': reset_url,
            }

            subject = "Password Reset Requested"
            email_template_name = "registration/password_reset_email.html"
            email_content = render_to_string(email_template_name, context)
            email = EmailMessage(subject, email_content, to=[user.email])
            email.send()

            return Response({"detail": "Password reset link sent to your email."}, status=status.HTTP_200_OK)

        return Response({"detail": "No user with the provided email."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been updated successfully."}, status=status.HTTP_200_OK)
