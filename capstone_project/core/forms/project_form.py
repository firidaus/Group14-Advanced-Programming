from django import forms
from core.models.project import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'program': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'facility': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'nature_of_project': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'rows': 4}),
            'innovation_focus': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'prototype_stage': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'testing_requirements': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'rows': 3}),
            'commercialization_plan': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'rows': 3}),
        }
