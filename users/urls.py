from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views.auth_views import CustomTokenObtainPairView, LogoutView
from users.views.user_views import UserProfileView, UserRegistrationView, DeleteAccountView
from users.views.password_views import ChangePasswordView

app_name = 'users'

urlpatterns = [
    # Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User Profile
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),

    # Password Reset
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
