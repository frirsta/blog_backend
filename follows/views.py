from django.db import IntegrityError
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.permissions import IsFollowerOrReadOnly
from .serializers import FollowSerializer
from .models import Follow


class FollowListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.all()
        follower_id = self.request.query_params.get('follower_id')
        following_id = self.request.query_params.get('following_id')

        if follower_id:
            queryset = queryset.filter(follower_id=follower_id)
        elif following_id:
            queryset = queryset.filter(following_id=following_id)

        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(follower=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "You already follow this user."})


class FollowDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsFollowerOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'pk'
