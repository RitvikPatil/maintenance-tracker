from django.contrib import admin
from .models import MaintenanceType, MaintenanceRecord, Reminder

@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'recommended_interval_km', 'recommended_interval_months')
    search_fields = ('name', 'description')
    list_filter = ('recommended_interval_km', 'recommended_interval_months')

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_type', 'date_performed', 'status', 'cost')
    list_filter = ('status', 'maintenance_type', 'date_performed')
    search_fields = ('vehicle__make', 'vehicle__model_name', 'notes', 'service_provider')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_performed'
    fieldsets = (
        (None, {
            'fields': ('vehicle', 'maintenance_type', 'status')
        }),
        ('Service Details', {
            'fields': ('date_performed', 'mileage_at_service', 'cost', 'service_provider')
        }),
        ('Next Service', {
            'fields': ('next_due_date', 'next_due_mileage')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('maintenance_record', 'due_date', 'is_completed')
    list_filter = ('is_completed', 'due_date')
    search_fields = ('maintenance_record__vehicle__make', 'maintenance_record__vehicle__model_name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'due_date'
