# core/models/participant.py
from django.db import models

class Participant(models.Model):
    # Affiliation choices
    AFFILIATION_CHOICES = [
        ('CS', 'Computer Science'),
        ('SE', 'Software Engineering'),
        ('Engineering', 'Engineering'),
        ('Other', 'Other'),
    ]
    
    # Specialization choices
    SPECIALIZATION_CHOICES = [
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Business', 'Business'),
    ]
    
    # Institution choices
    INSTITUTION_CHOICES = [
        ('SCIT', 'SCIT'),
        ('CEDAT', 'CEDAT'),
        ('UniPod', 'UniPod'),
        ('UIRI', 'UIRI'),
        ('Lwera', 'Lwera'),
    ]
    
    # Fields as per Table 1.6
    ParticipantId = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=50, choices=AFFILIATION_CHOICES)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    cross_skill_trained = models.BooleanField(default=False, help_text="Indicates cross-skill training")
    institution = models.CharField(max_length=50, choices=INSTITUTION_CHOICES)
    
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
    
    def __str__(self):
        return f"{self.full_name} ({self.affiliation})"
