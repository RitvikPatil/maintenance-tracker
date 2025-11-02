from rest_framework import serializers
from .models import MaintenanceType, MaintenanceRecord, Reminder
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer

class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    maintenance_type = MaintenanceTypeSerializer(read_only=True)
    maintenance_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MaintenanceType.objects.all(),
        source='maintenance_type',
        write_only=True
    )
    vehicle = serializers.SerializerMethodField()
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source='vehicle',
        write_only=True
    )
    reminders = ReminderSerializer(many=True, read_only=True)
    
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'vehicle', 'vehicle_id', 'maintenance_type', 'maintenance_type_id',
            'date_performed', 'mileage_at_service', 'cost', 'service_provider',
            'notes', 'next_due_date', 'next_due_mileage', 'status',
            'created_at', 'updated_at', 'reminders'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'reminders')
    
    def get_vehicle(self, obj):
        from vehicles.serializers import VehicleListSerializer
        return VehicleListSerializer(obj.vehicle, context=self.context).data

class MaintenanceRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class MaintenanceRecordListSerializer(serializers.ModelSerializer):
    maintenance_type = MaintenanceTypeSerializer()
    vehicle = serializers.StringRelatedField()
    
    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'vehicle', 'maintenance_type', 'date_performed',
            'mileage_at_service', 'cost', 'status', 'next_due_date'
        ]

class ReminderListSerializer(serializers.ModelSerializer):
    maintenance_record = serializers.StringRelatedField()
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'maintenance_record', 'due_date',
            'is_completed', 'notes'
        ]
        read_only_fields = ('id',)
