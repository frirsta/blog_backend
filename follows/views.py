from django.db import IntegrityError
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from blog.permissions import IsAuthorOrReadOnly
from .models import Follow
from .serializers import FollowSerializer


class FollowListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(follower=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "You already follow this user."})


class FollowDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'pk'
