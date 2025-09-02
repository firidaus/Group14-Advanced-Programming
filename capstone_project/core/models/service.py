# core/models/service.py
from django.db import models
from core.models.Faciltymodels import Facility

class Service(models.Model):
    # Category choices based on your specification
    CATEGORY_CHOICES = [
        ('Machining', 'Machining'),
        ('Testing', 'Testing'),
        ('Training', 'Training'),
    ]
    
    # Skill type choices based on your specification
    SKILL_TYPE_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Integration', 'Integration'),
    ]
    
    # Fields as per Table 1.3
    ServiceId = models.AutoField(primary_key=True)
    FacilityId = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    skill_type = models.CharField(max_length=50, choices=SKILL_TYPE_CHOICES)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return f"{self.name} - {self.FacilityId.name}"