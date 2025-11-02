from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

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
        return MaintenanceRecord.objects.filter(vehicle__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return MaintenanceRecordListSerializer
        elif self.action == 'create':
            return MaintenanceRecordCreateSerializer
        return MaintenanceRecordSerializer

    def perform_create(self, serializer):
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

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming maintenance records"""
        upcoming_records = self.get_queryset().filter(
            next_due_date__gte=timezone.now().date()
        ).order_by('next_due_date')
        
        page = self.paginate_queryset(upcoming_records)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(upcoming_records, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_reminder(self, request, pk=None):
        """Create a reminder for a maintenance record"""
        maintenance_record = self.get_object()
        serializer = ReminderSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(maintenance_record=maintenance_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReminderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing maintenance reminders"""
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_completed']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        return Reminder.objects.filter(
            maintenance_record__vehicle__user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ReminderListSerializer
        return ReminderSerializer

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a reminder as completed"""
        reminder = self.get_object()
        reminder.is_completed = True
        reminder.save()
        return Response({'status': 'reminder marked as completed'})

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming reminders"""
        upcoming_reminders = self.get_queryset().filter(
            is_completed=False,
            due_date__gte=timezone.now().date()
        ).order_by('due_date')
        
        page = self.paginate_queryset(upcoming_reminders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(upcoming_reminders, many=True)
        return Response(serializer.data)
