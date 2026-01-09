from django.db import models
from companies.models import Company


class InterviewPrep(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='prep')
    self_intro = models.TextField(blank=True, null=True)
    why_apply = models.TextField(blank=True, null=True)
    questions_to_ask = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prep for {self.company.name}"
