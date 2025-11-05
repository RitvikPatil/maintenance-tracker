import logging

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

logger = logging.getLogger(__name__)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.

    This serializer is used to validate the old password and new password
    submitted by the user. The new password is validated using the
    django.contrib.auth.password_validation module.

    Attributes:
        old_password (str): The user's old password.
        new_password (str): The user's new password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        """
        Validate the new password.

        This method uses the django.contrib.auth.password_validation module
        to validate the new password.

        Args:
            value (str): The new password to validate.

        Returns:
            str: The validated new password.
        """
        logger.debug("Validating new password")
        validate_password(value)
        logger.info("New password validated")
        return value
