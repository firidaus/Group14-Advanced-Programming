from django.db import models


class Program(models.Model):
        NATIONAL_ALIGNMENT_CHOICES = [
    ('NDPIII', 'NDPIII - National Development Plan III'),
    ('DigitalRoadmap2023_2028', 'Digital Roadmap 2023-2028'),
    ('4IR', '4IR - Fourth Industrial Revolution'),
]
        
        FOCUS_AREAS_CHOICES = [
    ('IoT', 'Internet of Things (IoT)'),
    ('Automation', 'Automation'),
    ('Renewable Energy', 'Renewable Energy'),
    ('AI', 'Artificial Intelligence'),
    ('Machine Learning', 'Machine Learning'),
    ('Robotics', 'Robotics'),
    ('Smart Cities', 'Smart Cities'),
]
        
        PHASES_CHOICES = [
    ('Cross-Skilling', 'Cross-Skilling'),
    ('Collaboration', 'Collaboration'),
    ('Technical Skills', 'Technical Skills'),
    ('Prototyping', 'Prototyping'),
    ('Commercialization', 'Commercialization'),
]
        ProgramId = models.AutoField(primary_key=True)
        name = models.CharField(max_length=200, unique=True)
        description = models.TextField(blank=True)
        national_alignment = models.CharField(max_length=50, choices=NATIONAL_ALIGNMENT_CHOICES, blank=True)
        focus_areas = models.CharField(max_length=50, choices=FOCUS_AREAS_CHOICES, blank=True)
        phases = models.CharField(max_length=50, choices=PHASES_CHOICES, blank=True)
        
        start_date = models.DateField(null=True, blank=True)
        end_date = models.DateField(null=True, blank=True)
        active = models.BooleanField(default=True)

        class Meta:
                ordering = ["-start_date", "name"]
                verbose_name = "Program"
                verbose_name_plural = "Programs"

        def __str__(self) -> str:
                return f"{self.name}"

"""Program (Table 1.1)

        Fields:
            - ProgramId (PK)
            - name
            - description
            - national_alignment
            - focus_areas
            - phases
            - start_date, end_date, active

 Relationship: One Program has many Projects (FKs will live on Project model). """