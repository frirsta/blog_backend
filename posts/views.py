from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import permissions, generics, filters
from rest_framework.parsers import MultiPartParser, FormParser
from blog.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CategorySerializer, TagSerializer
from .models import Post, Tag, Category


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['likes__user__profile',
                        'author__profile', 'category', 'category__id', 'category__name', 'tags', 'tags__id']
    ordering_fields = ['created_at', 'likes_count',
                       'comments_count', 'category__name']
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
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['likes__user__profile',
                        'author__profile', 'category', 'category__id', 'category__name', 'tags', 'tags__id']
    ordering_fields = ['created_at', 'likes_count',
                       'comments_count', 'category__name']


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return Post.objects.filter(author=user)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
