from rest_framework import permissions, generics, filters
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from blog.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from .models import Post


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['likes__user__profile', 'author__profile']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception as e:
            print(f"Error while saving post: {str(e)}")
            raise


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['likes__user__profile', 'author__profile']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return Post.objects.filter(author=user)
