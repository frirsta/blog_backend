from django.urls import path
from .views import PostListCreateView, PostDetail, UserPostListView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('user/<int:user_id>/', UserPostListView.as_view(), name='user-posts'),
]
