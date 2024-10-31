from rest_framework import generics
from .models import Follow
from .serializers import FollowSerializer
from blog.permissions import IsAuthorOrReadOnly


class FollowDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
