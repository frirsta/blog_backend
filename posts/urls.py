from django.urls import path
from .views import PostListView, PostDetail


urlpatterns = [
    path('', PostListView.as_view(), name='post-detail'),
    path('<int:id>/', PostDetail.as_view(), name='post-detail-other'),
]
