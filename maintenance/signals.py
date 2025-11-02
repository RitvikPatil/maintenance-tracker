from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import MaintenanceRecord, Reminder

@receiver(post_save, sender=MaintenanceRecord)
def create_or_update_reminder(sender, instance, created, **kwargs):
    """
    Create or update a reminder when a maintenance record is saved.
    """
    if instance.next_due_date:
        Reminder.objects.update_or_create(
            maintenance_record=instance,
            defaults={
                'due_date': instance.next_due_date,
                'is_completed': False,
                'notes': f"Upcoming maintenance for {instance.vehicle} - {instance.maintenance_type}"
            }
        )

@receiver(pre_save, sender=MaintenanceRecord)
def update_vehicle_mileage(sender, instance, **kwargs):
    """
    Update the vehicle's current mileage when a maintenance record is saved.
    """
    if instance.mileage_at_service and instance.vehicle:
        if instance.mileage_at_service > instance.vehicle.current_mileage:
            instance.vehicle.current_mileage = instance.mileage_at_service
            instance.vehicle.save(update_fields=['current_mileage'])