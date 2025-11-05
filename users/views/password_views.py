import logging

from rest_framework import status, generics, permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from users.serializers.password_serializers import ChangePasswordSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing user password"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        logger.debug(f"Getting user object for password change | User_id: {self.request.user.id}")
        return self.request.user

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating user password | User_id: {self.request.user.id}")
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                logger.error(f"Wrong password provided | User_id: {self.request.user.id}")
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            
            logger.info(f"Password updated successfully | User_id: {self.request.user.id}")
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        
        logger.error(f"Invalid password data provided | User_id: {self.request.user.id}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
