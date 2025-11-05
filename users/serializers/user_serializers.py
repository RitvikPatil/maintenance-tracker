import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Set up logging
logger = logging.getLogger(__name__)
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and creation of new user accounts.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password],
        help_text="Password must meet complexity requirements"
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        """
        Create and return a new user instance.
        
        Args:
            validated_data (dict): Validated user data
            
        Returns:
            User: The created user instance
        """
        try:
            logger.info(f"Creating new user with email: {validated_data['email']}")
            user = User.objects.create_user(**validated_data)
            logger.info(f"User {user.email} created successfully")
            return user
        except Exception as e:
            logger.error(f"Failed to create user {validated_data.get('email')}: {str(e)}")
            raise

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile operations.
    Handles retrieval of user profile information.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')