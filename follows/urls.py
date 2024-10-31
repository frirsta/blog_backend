from django.urls import path
from .views import FollowDetail, FollowListView

urlpatterns = [
    path('<int:pk>/', FollowDetail.as_view(), name='follow-user'),
    path('', FollowListView.as_view(), name='follow-list'),
]
