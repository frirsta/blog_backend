from django.urls import path
from .views import ProfileListView, ProfileDetailView, UserRegistrationView, PasswordResetAPIView, PasswordResetConfirmAPIView, ChangePasswordView, CurrentUserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('', ProfileListView.as_view(), name='profile-list'),
    path('<int:pk>/', ProfileDetailView.as_view(),
         name='profile-detail-other'),
    path('password-reset/', PasswordResetAPIView.as_view(),
         name='password-reset-api'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(),
         name='password-reset-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('current/', CurrentUserProfileView.as_view(),
         name='current_user_profile'),
]
