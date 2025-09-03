from django.db import models
from core.models.project import Project


class Outcome(models.Model):
    OutcomeId = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="outcomes")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    artifact_link = models.URLField(blank=True)

    outcome_type = models.CharField(max_length=100, choices=[
        ("CAD", "CAD"),
        ("PCB", "PCB"),
        ("Prototype", "Prototype"),
        ("Report", "Report"),
        ("Business Plan", "Business Plan"),
    ])
   
    quality_certification = models.CharField(max_length=200, blank=True)
    commercialization_status = models.CharField(max_length=100, choices=[
        ("Demoed", "Demoed"),
        ("Market Linked", "Market Linked"),
        ("Launched", "Launched"),
    ])

    class Meta:
        verbose_name = "Outcome"
        verbose_name_plural = "Outcomes"

    def __str__(self):
        return f"{self.title} ({self.project.title})"
