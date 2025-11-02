from django.utils.translation import gettext_lazy as _
from vehicles.models import Vehicle
from common.models import BaseModel
from django.db import models

class MaintenanceType(BaseModel):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    recommended_interval_km = models.PositiveIntegerField(
        _('recommended interval (km)'), 
        null=True, 
        blank=True,
        help_text=_('Recommended interval in kilometers')
    )
    recommended_interval_months = models.PositiveIntegerField(
        _('recommended interval (months)'), 
        null=True, 
        blank=True,
        help_text=_('Recommended interval in months')
    )
    
    class Meta:
        verbose_name = _('maintenance type')
        verbose_name_plural = _('maintenance types')
    
    def __str__(self):
        return self.name


class MaintenanceRecord(models.Model):
    """Model for tracking maintenance activities performed on vehicles"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name=_('vehicle')
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name='maintenance_records',
        verbose_name=_('maintenance type')
    )
    date_performed = models.DateField(_('date performed'))
    mileage_at_service = models.PositiveIntegerField(_('mileage at service'))
    cost = models.DecimalField(
        _('cost'),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    service_provider = models.CharField(
        _('service provider'),
        max_length=200,
        blank=True
    )
    notes = models.TextField(_('notes'), blank=True)
    next_due_date = models.DateField(
        _('next due date'),
        null=True,
        blank=True,
        help_text=_('Next scheduled date for this maintenance')
    )
    next_due_mileage = models.PositiveIntegerField(
        _('next due mileage'),
        null=True,
        blank=True,
        help_text=_('Next scheduled mileage for this maintenance')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('maintenance record')
        verbose_name_plural = _('maintenance records')
        ordering = ['-date_performed', '-created_at']
    
    def __str__(self):
        return f"{self.maintenance_type} - {self.vehicle} ({self.date_performed})"


class Reminder(models.Model):
    """Model for maintenance reminders"""
    maintenance_record = models.ForeignKey(
        MaintenanceRecord,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name=_('maintenance record')
    )
    due_date = models.DateField(_('due date'))
    is_completed = models.BooleanField(_('is completed'), default=False)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('reminder')
        verbose_name_plural = _('reminders')
        ordering = ['due_date', '-is_completed']
    
    def __str__(self):
        return f"Reminder for {self.maintenance_record} - Due: {self.due_date}"
