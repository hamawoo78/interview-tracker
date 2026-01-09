from django import forms
from .models import InterviewEvent


class InterviewEventForm(forms.ModelForm):
    class Meta:
        model = InterviewEvent
        fields = [
            'start_datetime', 'interviewer_name',
            'interview_type', 'meeting_link', 'notes'
        ]
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            # 'end_datetime': forms.DateTimeInput(attrs={
            #     'class': 'form-control',
            #     'type': 'datetime-local'
            # }),
            'interviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Interviewer name'
            }),
            'interview_type': forms.Select(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Interview notes'
            }),
        }
