from django import forms
from core.models.Outcome import Outcome


class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = [
            "project",
            "title",
            "description",
            "artifact_link",
            "outcome_type",
            "quality_certification",
            "commercialization_status",
        ]
        widgets = {
            "project": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "description": forms.Textarea(attrs={"class": "w-full p-2 border rounded"}),
            "artifact_link": forms.URLInput(attrs={"class": "w-full p-2 border rounded"}),
            "outcome_type": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
            "quality_certification": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "commercialization_status": forms.Select(attrs={"class": "w-full p-2 border rounded"}),
        }
