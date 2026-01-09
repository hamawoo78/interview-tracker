from django.db import models
from django.utils import timezone


class Company(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interview')
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    position_title = models.CharField(max_length=255, blank=True, null=True)
    job_description_url = models.URLField(blank=True, null=True)
    job_description_file = models.FileField(upload_to='job_descriptions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name

    def get_latest_interview(self):
        """Get the most recent interview event for this company."""
        from interviews.models import InterviewEvent
        return InterviewEvent.objects.filter(company=self).order_by('-start_datetime').first()
