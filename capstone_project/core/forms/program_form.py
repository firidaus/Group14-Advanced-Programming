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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'rows': 4}),
            'national_alignment': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'focus_areas': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'phases': forms.Select(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm'}),
            'start_date': forms.DateInput(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'mt-1 block w-full rounded border-gray-300 shadow-sm', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
        }
