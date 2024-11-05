from django.urls import path
from .views import LikeListCreateAPIView, LikeDetailsAPIView

urlpatterns = [
    path('', LikeListCreateAPIView.as_view(), name='like_list_create'),
    path('<int:pk>/', LikeDetailsAPIView.as_view(), name='like_details'),
]
