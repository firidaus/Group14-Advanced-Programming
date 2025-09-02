from django import forms
from core.models.Equipment import Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name',
            'capabilities',
            'description',
            'inventory_code',
            'usage_domain',
            'support_phase',
            'facility',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter equipment name'
            }),
            'capabilities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter key capabilities'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter equipment description'
            }),
            'inventory_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter inventory tracking code'
            }),
            'usage_domain': forms.Select(attrs={
                'class': 'form-control'
            }),
            'support_phase': forms.Select(attrs={
                'class': 'form-control'
            }),
            'facility': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
