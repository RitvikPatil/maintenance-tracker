from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import logging

from users.serializers.auth_serializers import CustomTokenObtainPairSerializer

logger = logging.getLogger(__name__)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view to use our custom serializer"""
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    """View for user logout"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
