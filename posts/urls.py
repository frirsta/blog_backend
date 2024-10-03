from django.urls import path
from .views import PostListCreate, PostDetail

urlpatterns = [
    path('', PostListCreate.as_view(), name='post-list-create'),  # For listing and creating posts
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),   # For retrieving, updating, and deleting a post
]