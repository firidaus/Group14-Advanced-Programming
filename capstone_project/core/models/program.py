from django.db import models


class Program(models.Model):

        ProgramId = models.AutoField(primary_key=True)
        name = models.CharField(max_length=200, unique=True)
        description = models.TextField(blank=True)
        national_alignment = models.CharField(max_length=200, blank=True)
        focus_areas = models.TextField(blank=True)
        phases = models.TextField(blank=True)
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