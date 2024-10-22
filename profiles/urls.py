from django.urls import path
from .views import ProfileDetailView, AccountDeleteView, UserRegistrationView, PasswordResetAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('', ProfileDetailView.as_view(),
         name='profile-detail'),  # logged-in user
    path('<int:user_id>/', ProfileDetailView.as_view(),
         name='profile-detail-other'),
    path('delete/', AccountDeleteView.as_view(), name='account-delete'),
    path('password-reset/', PasswordResetAPIView.as_view(),
         name='password-reset-api'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(),
         name='password-reset-confirm'),
]
