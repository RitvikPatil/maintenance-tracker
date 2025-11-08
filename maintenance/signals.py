from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import logging

from .models import MaintenanceRecord, Reminder

logger = logging.getLogger(__name__)

@receiver(post_save, sender=MaintenanceRecord)
def create_or_update_reminder(sender, instance, created, **kwargs):
    """
    Create, update, or delete a reminder when a maintenance record is saved.
    """
    try:
        with transaction.atomic():
            if instance.next_due_date:
                # Create or update the reminder
                Reminder.objects.update_or_create(
                    maintenance_record=instance,
                    defaults={
                        'due_date': instance.next_due_date,
                        'is_completed': False,
                        'notes': f"Upcoming maintenance for {instance.vehicle} - {instance.maintenance_type}"
                    }
                )
                logger.info(f"Updated/created reminder for maintenance record {instance.id}")
            else:
                # Delete any existing reminders if next_due_date is removed
                deleted_count, _ = instance.reminders.all().delete()
                if deleted_count:
                    logger.info(f"Deleted {deleted_count} reminder(s) for maintenance record {instance.id}")
    except Exception as e:
        logger.error(f"Error in create_or_update_reminder for maintenance record {instance.id}: {str(e)}")
        # Re-raise the exception to ensure the transaction is rolled back
        raise

@receiver(pre_save, sender=MaintenanceRecord)
def update_vehicle_mileage(sender, instance, **kwargs):
    """
    Update the vehicle's current mileage when a maintenance record is saved.
    Only updates if the new mileage is higher than the current mileage.
    """
    try:
        if instance.mileage_at_service is not None and instance.vehicle:
            # Ensure mileage is not negative
            if instance.mileage_at_service < 0:
                raise ValidationError({
                    'mileage_at_service': 'Mileage cannot be negative.'
                })
                
            # Only update if the new mileage is higher than current
            if instance.mileage_at_service > instance.vehicle.current_mileage:
                logger.info(
                    f"Updating vehicle {instance.vehicle.id} mileage from "
                    f"{instance.vehicle.current_mileage} to {instance.mileage_at_service}"
                )
                instance.vehicle.current_mileage = instance.mileage_at_service
                # Only save if the vehicle isn't being created
                if not instance.vehicle._state.adding:
                    instance.vehicle.save(update_fields=['current_mileage'])
    except Exception as e:
        logger.error(f"Error in update_vehicle_mileage for maintenance record {instance.id}: {str(e)}")
        # Re-raise the exception to ensure the transaction is rolled back
        raise