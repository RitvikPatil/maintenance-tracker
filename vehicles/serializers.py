from rest_framework import serializers
from .models import Vehicle, VehicleImage
from users.models import User


class VehicleImageSerializer(serializers.ModelSerializer):
    """Serializer for vehicle images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'image_url', 'caption', 'is_primary', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle model"""
    images = VehicleImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True,
        required=False
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'user', 'make', 'model_name', 'registration_number',
            'vehicle_type', 'year', 'color', 'vin_number', 'purchase_date',
            'current_mileage', 'created_at', 'updated_at', 'images', 'uploaded_images'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create a new vehicle with optional images"""
        uploaded_images = validated_data.pop('uploaded_images', [])
        vehicle = Vehicle.objects.create(**validated_data)
        
        # Handle uploaded images
        for image in uploaded_images:
            VehicleImage.objects.create(vehicle=vehicle, image=image)
            
        return vehicle
    
    def update(self, instance, validated_data):
        """Update a vehicle and handle image uploads"""
        uploaded_images = validated_data.pop('uploaded_images', None)
        
        # Update vehicle fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle new image uploads if any
        if uploaded_images is not None:
            for image in uploaded_images:
                VehicleImage.objects.create(vehicle=instance, image=image)
        
        return instance


class VehicleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing vehicles"""
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'make', 'model_name', 'registration_number',
            'vehicle_type', 'year', 'primary_image'
        ]
    
    def get_primary_image(self, obj):
        """Get the URL of the primary image if available"""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image and primary_image.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(primary_image.image.url)
        return None
