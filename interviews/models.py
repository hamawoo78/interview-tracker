from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from companies.models import Company


class InterviewEvent(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('technical', 'Technical'),
        ('onsite', 'Onsite'),
        ('online', 'Online'),
        ('hr', 'HR'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interviews')
    start_datetime = models.DateTimeField()
    # end_datetime = models.DateTimeField(blank=True, null=True)
    interviewer_name = models.CharField(max_length=255, blank=True, null=True)
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return f"{self.company.name} - {self.start_datetime}"
