from django import forms
from core.models.participant import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            "full_name",
            "email",
            "affiliation",
            "specialization",
            "cross_skill_trained",
            "institution",
            "project",
        ]
