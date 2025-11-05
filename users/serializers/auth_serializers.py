from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer that extends the default JWT token serializer
    to include additional user details in the authentication response.
    """
    
    def validate(self, attrs):
        """
        Validate user credentials and return authentication tokens with user details.
        
        Args:
            attrs (dict): Dictionary containing the request data (email and password)
            
        Returns:
            dict: Dictionary containing:
                - refresh: JWT refresh token
                - access: JWT access token
                - user: Dictionary containing user details
                
        Raises:
            AuthenticationFailed: If the credentials are invalid
        """
        try:
            logger.debug(f"Attempting authentication for email: {attrs.get('email')}")
            
            # Get the default token data
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            
            # Add user details to the response
            user_data = {
                'id': self.user.id,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'is_staff': self.user.is_staff,
                'is_active': self.user.is_active
            }
            
            # Construct the response data
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }
            
            logger.info(f"User {self.user.email} authenticated successfully")
            return response_data
            
        except Exception as e:
            logger.error(f"Authentication failed for email {attrs.get('email')}: {str(e)}")
            raise
