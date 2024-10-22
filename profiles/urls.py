from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileDetailView, AccountDeleteView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('', ProfileDetailView.as_view(),
         name='profile-detail'),  # logged-in user
    path('<int:user_id>/', ProfileDetailView.as_view(),
         name='profile-detail-other'),
    path('delete/', AccountDeleteView.as_view(), name='account-delete'),
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
