from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from .serializers import ProfileSerializer, UserRegistrationSerializer, PasswordResetSerializer
from .models import Profile


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user to register

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT token upon successful registration
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "detail": "User created successfully.",
                "refresh": str(refresh),  # JWT refresh token
                "access": str(access_token),  # JWT access token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')

        if user_id is None:
            return self.request.user.profile

        user = get_object_or_404(User, id=user_id)
        return user.profile

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        if user_id is not None and user_id != str(request.user.id):
            raise PermissionDenied(
                "You do not have permission to edit this profile.")

        return super().update(request, *args, **kwargs)


class AccountDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        Profile.objects.filter(user=user).delete()
        user.delete()

        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_200_OK)


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
            reset_url = f"http://127.0.0.1:3000/password-reset-confirm/{
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
