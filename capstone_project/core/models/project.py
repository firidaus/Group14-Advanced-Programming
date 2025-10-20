from django.db import models
from core.models.program import Program
from core.models.Facility import Facility


class Project(models.Model):
    ProjectId = models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="projects")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=200)
    nature_of_project = models.CharField(max_length=100, choices=[
        ("Research", "Research"),
        ("Prototype", "Prototype"),
        ("Applied Work", "Applied Work"),
    ])
    description = models.TextField(blank=True)
    innovation_focus = models.CharField(max_length=200,  choices=[
        ("IoT devices", "IoT devices"),
        ("Smart Home", "Smart Home"),
        ("Renewable Energy", "Renewable Energy"),
    ])
    prototype_stage = models.CharField(max_length=100, choices=[
        ("Concept", "Concept"),
        ("Prototype", "Prototype"),
        ("MVP", "MVP"),
        ("Market Launch", "Market Launch"),
    ])
    testing_requirements = models.TextField(blank=True)
    commercialization_plan = models.TextField(blank=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title
