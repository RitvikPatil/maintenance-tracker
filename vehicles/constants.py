from django.db import models
from django.utils.translation import gettext_lazy as _

class VehicleType(models.TextChoices):
    CAR = 'car', _('Car')
    MOTORCYCLE = 'motorcycle', _('Motorcycle')
    TRUCK = 'truck', _('Truck')
    SUV = 'suv', _('SUV')
    VAN = 'van', _('Van')
    OTHER = 'other', _('Other')

