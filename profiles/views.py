from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, UserRegistrationSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


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
