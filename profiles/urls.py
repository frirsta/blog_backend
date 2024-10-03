from django.urls import path
from .views import ProfileDetailView, AccountDeleteView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('', ProfileDetailView.as_view(), name='profile-detail'),  # logged-in user
    path('<int:user_id>/', ProfileDetailView.as_view(), name='profile-detail-other'),
    path('delete/', AccountDeleteView.as_view(), name='account-delete'),
]
