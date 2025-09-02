# core/forms/service_form.py
from django import forms
from core.models.service import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['FacilityId', 'name', 'description', 'category', 'skill_type']
        widgets = {
            'FacilityId': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'skill_type': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
        }