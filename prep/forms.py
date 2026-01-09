from django import forms
from .models import InterviewPrep


class InterviewPrepForm(forms.ModelForm):
    class Meta:
        model = InterviewPrep
        fields = ['self_intro', 'why_apply', 'questions_to_ask', 'additional_notes']
        widgets = {
            'self_intro': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your self-introduction'
            }),
            'why_apply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Why you applied to this company'
            }),
            'questions_to_ask': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Questions to ask the interviewer'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes'
            }),
        }
