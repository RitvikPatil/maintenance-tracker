from django.contrib import admin
from .models import Vehicle, VehicleImage

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model_name', 'registration_number', 'vehicle_type', 'year', 'user')
    list_filter = ('vehicle_type', 'year', 'make')
    search_fields = ('make', 'model_name', 'registration_number', 'vin_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'make', 'model_name', 'registration_number', 'vehicle_type')
        }),
        ('Additional Information', {
            'fields': ('year', 'color', 'vin_number', 'purchase_date', 'current_mileage'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    fieldsets = (
        (None, {
            'fields': ('vehicle', 'image', 'caption')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
