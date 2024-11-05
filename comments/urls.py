from django.urls import path
from .views import CommentListCreateView, CommentDetail


urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:pk>/', CommentDetail.as_view(), name='comment-detail')
]
