from django.db import models
from django.core.exceptions import ValidationError

# Predefined choices for partners and facility types
PARTNERS = [
    ('UniPod', 'UniPod'),
    ('UIRI', 'UIRI'),
    ('Lwera', 'Lwera'),
]

FACILITY_TYPES = [
    ('Laboratory', 'Laboratory'),
    ('Workshop', 'Workshop'),
    ('Testing Center', 'Testing Center'),
    ('Maker Space', 'Maker Space'),
]

# Since you no longer have a Capability model, store capabilities as text
CAPABILITIES_CHOICES = [
    ('CNC', 'CNC'),
    ('PCB Fabrication', 'PCB Fabrication'),
    ('Materials Testing', 'Materials Testing'),
]

class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    partner = models.CharField(max_length=50, choices=PARTNERS)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    capabilities = models.CharField(max_length=200, choices=CAPABILITIES_CHOICES)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name or not self.location:
            raise ValidationError("Name and Location are required.")