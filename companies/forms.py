from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'logo', 'website_url', 'location', 'status',
            'salary_min', 'salary_max', 'position_title',
            'job_description_url', 'job_description_file'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max salary'}),
            'position_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'}),
            'job_description_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'job_description_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
