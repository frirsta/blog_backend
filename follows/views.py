from rest_framework import permissions, generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Follow
from .serializers import FollowSerializer


class FollowUserView(generics.CreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, user_id):
        following = get_object_or_404(User, id=user_id)
        if request.user == following:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=following)
        if created:
            return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)
        return Response({"message": "Already following."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        following = get_object_or_404(User, id=user_id)
        follow = Follow.objects.filter(
            follower=request.user, following=following).first()
        if follow:
            follow.delete()
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not following this user."}, status=status.HTTP_400_BAD_REQUEST)


class FollowListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['follower', 'following']
    ordering_fields = ['created_at']
