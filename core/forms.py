from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['timezone', 'auto_detect_timezone']
        widgets = {
            'timezone': forms.Select(attrs={'class': 'form-control'}),
            'auto_detect_timezone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
