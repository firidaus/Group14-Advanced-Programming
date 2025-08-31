# core/forms.py

from django import forms
from core.models import Facility

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ["name", "location", "description", "partner", "facility_type", "capabilities"]
