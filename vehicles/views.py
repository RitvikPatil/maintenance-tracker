import logging

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Vehicle, VehicleImage
from .serializers import (
    VehicleSerializer,
    VehicleListSerializer,
    VehicleImageSerializer
)
from users.models import User

logger = logging.getLogger(__name__)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vehicles.
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['vehicle_type', 'make', 'year']
    search_fields = ['make', 'model_name', 'registration_number', 'vin_number']
    ordering_fields = ['make', 'model_name', 'year', 'purchase_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return only the vehicles owned by the current user."""
        logger.info('Fetching vehicles | user_id: %s', self.request.user.id)
        return Vehicle.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return VehicleListSerializer
        return VehicleSerializer

    def perform_create(self, serializer):
        """Set the current user as the owner of the vehicle."""
        logger.info('Creating vehicle for user | user_id: %s', self.request.user.id)
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image for a vehicle."""
        logger.info(f'Uploading image for vehicle | vehicle_id: {pk}')
        vehicle = self.get_object()
        serializer = VehicleImageSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(vehicle=vehicle)
            logger.info('Image uploaded successfully | vehicle_id: %s', pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Image upload failed | vehicle_id: %s', pk)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='set-primary-image/(?P<image_id>[^/.]+)')
    def set_primary_image(self, request, pk=None, image_id=None):
        """Set an image as the primary image for a vehicle."""
        logger.info('Setting primary image for vehicle | vehicle_id: %s', pk)
        vehicle = self.get_object()
        try:
            image = vehicle.images.get(id=image_id)
            image.is_primary = True
            image.save()
            logger.info('Primary image set successfully | vehicle_id: %s', pk)
            return Response({'status': 'primary image set'})
        except VehicleImage.DoesNotExist:
            logger.error('Image not found | vehicle_id: %s', pk)
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['delete'], url_path='delete-image/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        """Delete an image from a vehicle."""
        logger.info('Deleting image for vehicle | vehicle_id: %s', pk)
        vehicle = self.get_object()
        try:
            image = vehicle.images.get(id=image_id)
            image.delete()
            logger.info('Image deleted successfully | vehicle_id: %s', pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except VehicleImage.DoesNotExist:
            logger.error('Image not found | vehicle_id: %s', pk)
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class VehicleImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vehicle images.
    """
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """Return only the images for vehicles owned by the current user."""
        logger.info('Fetching images for user | user_id: %s', self.request.user.id)
        return VehicleImage.objects.filter(vehicle__user=self.request.user)

    def get_vehicle(self):
        """Get the vehicle for the current request."""
        logger.info('Fetching vehicle | vehicle_id: %s', self.kwargs['vehicle_pk'])
        return get_object_or_404(
            Vehicle,
            id=self.kwargs['vehicle_pk'],
            user=self.request.user
        )

    def list(self, request, vehicle_pk=None):
        """List all images for a specific vehicle."""
        logger.info('Listing images for vehicle | vehicle_id: %s', vehicle_pk)
        vehicle = self.get_vehicle()
        images = vehicle.images.all()
        serializer = self.get_serializer(images, many=True, context={'request': request})
        logger.info('Images listed successfully | vehicle_id: %s', vehicle_pk)
        return Response(serializer.data)

    def create(self, request, vehicle_pk=None):
        """Upload a new image for a vehicle."""
        logger.info('Uploading image for vehicle | vehicle_id: %s', vehicle_pk)
        vehicle = self.get_vehicle()
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(vehicle=vehicle)
            logger.info('Image uploaded successfully | vehicle_id: %s', vehicle_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Image upload failed | vehicle_id: %s', vehicle_pk)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
