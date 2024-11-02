from django.urls import path
from .views import FollowDetailView, FollowCreateView

urlpatterns = [
    path('<int:pk>/', FollowDetailView.as_view(), name='follow-user'),
    path('', FollowCreateView.as_view(), name='follow-list'),
]
