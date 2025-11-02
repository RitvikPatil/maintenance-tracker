from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token obtain pair serializer to include user details in the response"""
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        # Add user details to the response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        
        # Add tokens to the response
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        return data
