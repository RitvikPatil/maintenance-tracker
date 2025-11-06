from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'maintenance'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'maintenance-types', views.MaintenanceTypeViewSet, basename='maintenance-type')
router.register(r'records', views.MaintenanceRecordViewSet, basename='maintenance-record')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')

urlpatterns = [
    # Include the default router URLs
    path('', include(router.urls)),
    
    # Additional maintenance record endpoints
    path(
        'records/upcoming/',
        views.MaintenanceRecordViewSet.as_view({'get': 'upcoming'}),
        name='upcoming-maintenance'
    ),
    path(
        'records/<int:pk>/create-reminder/',
        views.MaintenanceRecordViewSet.as_view({'post': 'create_reminder'}),
        name='create-maintenance-reminder'
    ),
    
    # Additional reminder endpoints
    path(
        'reminders/upcoming/',
        views.ReminderViewSet.as_view({'get': 'upcoming'}),
        name='upcoming-reminders'
    ),
    path(
        'reminders/<int:pk>/mark-completed/',
        views.ReminderViewSet.as_view({'post': 'mark_completed'}),
        name='mark-reminder-completed'
    ),
    path(
        'reminders/<int:pk>/mark-uncompleted/',
        views.ReminderViewSet.as_view({'post': 'mark_uncompleted'}),
        name='mark-reminder-uncompleted'
    ),
]
