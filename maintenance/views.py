from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import logging

from .models import MaintenanceType, MaintenanceRecord, Reminder
from .serializers import (
    MaintenanceTypeSerializer,
    MaintenanceRecordSerializer,
    MaintenanceRecordListSerializer,
    MaintenanceRecordCreateSerializer,
    ReminderSerializer,
    ReminderListSerializer
)
from vehicles.models import Vehicle

logger = logging.getLogger(__name__)

class MaintenanceTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing maintenance types"""
    queryset = MaintenanceType.objects.all()
    serializer_class = MaintenanceTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for managing maintenance records"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle', 'maintenance_type', 'status']
    search_fields = ['notes', 'service_provider']
    ordering_fields = ['date_performed', 'created_at', 'cost']
    ordering = ['-date_performed']

    def get_queryset(self):
        logger.info('Getting maintenance records for current user | user_id: %s', self.request.user.id)
        queryset = MaintenanceRecord.objects.filter(vehicle__user=self.request.user)
        logger.info('Maintenance records retrieved successfully | user_id: %s', self.request.user.id)
        return queryset

    def get_serializer_class(self):
        logger.info('Determining serializer class for action %s | user_id: %s', self.action, self.request.user.id)
        if self.action == 'list':
            serializer_class = MaintenanceRecordListSerializer
        elif self.action == 'create':
            serializer_class = MaintenanceRecordCreateSerializer
        else:
            serializer_class = MaintenanceRecordSerializer
        logger.info('Using serializer class %s | user_id: %s', serializer_class.__name__, self.request.user.id)
        return serializer_class

    def perform_create(self, serializer):
        logger.info('Creating new maintenance record | user_id: %s', self.request.user.id)
        serializer.save()
        # Update vehicle's last maintenance date and mileage
        vehicle = serializer.validated_data['vehicle']
        vehicle.last_maintenance_date = serializer.validated_data['date_performed']
        if 'mileage_at_service' in serializer.validated_data:
            vehicle.current_mileage = max(
                vehicle.current_mileage or 0,
                serializer.validated_data['mileage_at_service']
            )
        vehicle.save()
        logger.info('Maintenance record created successfully | user_id: %s', self.request.user.id)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming maintenance records"""
        logger.info('Getting upcoming maintenance records | user_id: %s', self.request.user.id)
        upcoming_records = self.get_queryset().filter(
            next_due_date__gte=timezone.now().date()
        ).order_by('next_due_date')
        
        page = self.paginate_queryset(upcoming_records)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(upcoming_records, many=True)
        logger.info('Upcoming maintenance records retrieved successfully | user_id: %s', self.request.user.id)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_reminder(self, request, pk=None):
        """Create a reminder for a maintenance record"""
        logger.info('Creating reminder for maintenance record %s | user_id: %s', pk, self.request.user.id)
        maintenance_record = self.get_object()
        serializer = ReminderSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(maintenance_record=maintenance_record)
            logger.info('Reminder created successfully | user_id: %s', self.request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Failed to create reminder | user_id: %s', self.request.user.id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        logger.info('Getting reminders for current user | user_id: %s', self.request.user.id)
        queryset = Reminder.objects.filter(
            maintenance_record__vehicle__user=self.request.user
        )
        logger.info('Reminders retrieved successfully | user_id: %s', self.request.user.id)
        return queryset

    def get_serializer_class(self):
        logger.info('Determining serializer class for action %s | user_id: %s', self.action, self.request.user.id)
        if self.action == 'list':
            serializer_class = ReminderListSerializer
        else:
            serializer_class = ReminderSerializer
        logger.info('Using serializer class %s | user_id: %s', serializer_class.__name__, self.request.user.id)
        return serializer_class

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a reminder as completed"""
        logger.info('Marking reminder %s as completed | user_id: %s', pk, self.request.user.id)
        reminder = self.get_object()
        reminder.is_completed = True
        reminder.save()
        logger.info('Reminder marked as completed successfully | user_id: %s', self.request.user.id)
        return Response({'status': 'reminder marked as completed'})

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming reminders"""
        logger.info('Getting upcoming reminders for current user | user_id: %s', self.request.user.id)
        upcoming_reminders = self.get_queryset().filter(
            is_completed=False,
            due_date__gte=timezone.now().date()
        ).order_by('due_date')
        
        page = self.paginate_queryset(upcoming_reminders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(upcoming_reminders, many=True)
        logger.info('Upcoming reminders retrieved successfully | user_id: %s', self.request.user.id)
        return Response(serializer.data)
