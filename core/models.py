from django.db import models
from django.contrib.auth.models import User
import pytz

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]


class UserProfile(models.Model):
    """Store user-specific settings including timezone preference."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    timezone = models.CharField(
        max_length=63,
        choices=TIMEZONE_CHOICES,
        default='America/New_York',
        help_text='User timezone for displaying dates and times'
    )
    auto_detect_timezone = models.BooleanField(
        default=True,
        help_text='Automatically detect timezone from IP address'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"
