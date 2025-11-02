from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'vehicles'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'', views.VehicleViewSet, basename='vehicle')

# Additional routes for vehicle images
vehicle_images = views.VehicleImageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    # Include the default router URLs
    path('', include(router.urls)),
    
    # Nested routes for vehicle images
    path('<int:vehicle_pk>/images/', vehicle_images, name='vehicle-images'),
    
    # Additional vehicle actions
    path(
        '<int:pk>/upload-image/', 
        views.VehicleViewSet.as_view({'post': 'upload_image'}), 
        name='vehicle-upload-image'
    ),
    path(
        '<int:pk>/set-primary-image/<int:image_id>/', 
        views.VehicleViewSet.as_view({'post': 'set_primary_image'}), 
        name='set-primary-image'
    ),
    path(
        '<int:pk>/delete-image/<int:image_id>/', 
        views.VehicleViewSet.as_view({'delete': 'delete_image'}), 
        name='delete-image'
    ),
]
