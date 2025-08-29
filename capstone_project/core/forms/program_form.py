from django import forms
from core.models import Program


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'name',
            'description',
            'national_alignment',
            'focus_areas',
            'phases',
            'start_date',
            'end_date',
            'active',
        ]
