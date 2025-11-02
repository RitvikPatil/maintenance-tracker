from django.utils.translation import gettext_lazy as _
from users.models import User
from common.models import BaseModel
from django.db import models

class Vehicle(BaseModel):
    class VehicleType(models.TextChoices):
        CAR = 'car', _('Car')
        MOTORCYCLE = 'motorcycle', _('Motorcycle')
        TRUCK = 'truck', _('Truck')
        SUV = 'suv', _('SUV')
        VAN = 'van', _('Van')
        OTHER = 'other', _('Other')

    # Required fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name=_('owner')
    )
    make = models.CharField(_('manufacturer'), max_length=100)
    model_name = models.CharField(_('model'), max_length=100)
    registration_number = models.CharField(
        _('registration number'),
        max_length=50,
        unique=True
    )
    vehicle_type = models.CharField(
        _('vehicle type'),
        max_length=20,
        choices=VehicleType.choices,
        default=VehicleType.CAR
    )
    
    # Optional fields
    year = models.PositiveIntegerField(_('year of manufacture'), null=True, blank=True)
    color = models.CharField(_('color'), max_length=50, blank=True)
    vin_number = models.CharField(
        _('VIN number'),
        max_length=17,
        blank=True,
        help_text=_('17-character Vehicle Identification Number')
    )
    purchase_date = models.DateField(_('purchase date'), null=True, blank=True)
    current_mileage = models.PositiveIntegerField(
        _('current mileage'),
        default=0,
        help_text=_('Current mileage in kilometers')
    )
    
    class Meta:
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')
        # ordering = ['-created_at']
        unique_together = ['user', 'registration_number']
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model_name} ({self.registration_number})"
    
    def save(self, *args, **kwargs):
        # Ensure VIN is uppercase and without spaces
        if self.vin_number:
            self.vin_number = self.vin_number.upper().replace(" ", "")
        super().save(*args, **kwargs)


class VehicleImage(models.Model):
    """Model for storing vehicle images"""
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('vehicle')
    )
    image = models.ImageField(
        _('image'),
        upload_to='vehicles/images/'
    )
    caption = models.CharField(_('caption'), max_length=255, blank=True)
    is_primary = models.BooleanField(_('primary image'), default=False)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('vehicle image')
        verbose_name_plural = _('vehicle images')
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image of {self.vehicle} ({self.id})"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset any other primary images for this vehicle
        if self.is_primary:
            VehicleImage.objects.filter(
                vehicle=self.vehicle,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
