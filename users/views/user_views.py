import logging

from rest_framework import status, generics, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from users.serializers.user_serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"User registration request received | User_id: {self.request.user.id}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully.'
        }
        
        logger.info(f"User {user.email} registered successfully | User_id: {user.id}")
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View to retrieve and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        logger.debug(f"Getting user object for profile | User_id: {self.request.user.id}")
        return self.request.user


class DeleteAccountView(generics.DestroyAPIView):
    """View for user account deletion with password confirmation"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer  # For schema generation

    def get_object(self):
        logger.debug(f"Getting user object for account deletion | User_id: {self.request.user.id}")
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Get password from request data
        password = request.data.get('password')
        if not password:
            logger.error(f"Password not provided for user {user.email} | User_id: {user.id}")
            return Response(
                {"password": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify password
        if not user.check_password(password):
            logger.error(f"Incorrect password provided for user {user.email} | User_id: {user.id}")
            return Response(
                {"password": ["Incorrect password."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the user
        user.delete()
        
        logger.info(f"User {user.email} deleted successfully | User_id: {user.id}")
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
