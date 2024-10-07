from django.urls import path
from .views import PostListCreateView, PostDetail


urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
