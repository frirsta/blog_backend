from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from blog.permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, CommentDetailSerializer
from .models import Comment


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'user__comment__user__profile']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
