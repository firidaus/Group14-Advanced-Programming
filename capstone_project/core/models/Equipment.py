from django.db import models
from .Faciltymodels import Facility

# Choices for usage domain
USAGE_DOMAIN_CHOICES = [
    ('Research', 'Research'),
    ('Development', 'Development'),
    ('Testing', 'Testing'),
    ('Production', 'Production'),
    ('Education', 'Education'),
]

# Choices for support phase
SUPPORT_PHASE_CHOICES = [
    ('Prototype', 'Prototype'),
    ('Development', 'Development'),
    ('Testing', 'Testing'),
    ('Production', 'Production'),
    ('Maintenance', 'Maintenance'),
]

class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    capabilities = models.TextField(blank=True, help_text="Key capabilities of this equipment")
    description = models.TextField(blank=True)
    inventory_code = models.CharField(max_length=50, unique=True, help_text="Unique inventory tracking code")
    usage_domain = models.CharField(max_length=50, choices=USAGE_DOMAIN_CHOICES)
    support_phase = models.CharField(max_length=50, choices=SUPPORT_PHASE_CHOICES)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='equipment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.name} ({self.inventory_code})"
