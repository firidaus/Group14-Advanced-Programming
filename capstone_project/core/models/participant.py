from django.db import models
from core.models.project import Project


class Participant(models.Model):
    ParticipantId = models.AutoField(primary_key=True)

    # One-to-many: each participant is linked to one project,
    # but a project can have many participants
    project = models.ForeignKey(Project,on_delete=models.CASCADE,  related_name="participants" )

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)

    specialization = models.CharField(max_length=50, choices=[
        ("CS", "Computer Science"),
        ("SE", "Software Engineering"),
        ("ENG", "Engineering"),
        ("OTH", "Other"),
    ])

    cross_skill_trained = models.BooleanField(default=False)

    institution = models.CharField(max_length=50, choices=[
        ("SCIT", "SCIT"),
        ("CEDAT", "CEDAT"),
        ("UNIPOD", "UniPod"),
        ("UIRI", "UIRI"),
        ("LWERA", "Lwera"),
    ])

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return f"{self.full_name} ({self.project.title})"
