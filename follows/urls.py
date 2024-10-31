from django.urls import path
from .views import FollowUserView, FollowListView

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('', FollowListView.as_view(), name='follow-list'),
]
