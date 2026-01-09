from django.utils import timezone
from django.conf import settings
import logging
import pytz
from .timezone_utils import get_timezone_from_ip, get_client_ip

logger = logging.getLogger(__name__)


class TimezoneMiddleware:
    """
    Middleware to set user timezone based on:
    1. User profile preference (if auto_detect_timezone is False)
    2. IP address geolocation (if auto_detect_timezone is True)
    3. Default timezone (fallback)
    
    Uses free geolocation API to detect timezone from IP.
    Falls back to default timezone if detection fails.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                # Get timezone for this user
                user_tz = self.get_user_timezone(request)
                
                if user_tz:
                    timezone.activate(user_tz)
                    request.timezone = str(user_tz)
                else:
                    timezone.activate(settings.TIME_ZONE)
                    request.timezone = settings.TIME_ZONE
            except Exception as e:
                logger.warning(f"Error setting timezone: {e}")
                timezone.activate(settings.TIME_ZONE)
                request.timezone = settings.TIME_ZONE
        else:
            timezone.activate(settings.TIME_ZONE)
            request.timezone = settings.TIME_ZONE

        response = self.get_response(request)
        return response

    @staticmethod
    def get_user_timezone(request):
        """
        Get timezone for user based on profile settings and IP detection.
        
        Returns:
            pytz timezone object or None
        """
        try:
            # Get or create user profile
            profile = request.user.profile
        except Exception:
            # Profile doesn't exist, create it
            from .models import UserProfile
            profile = UserProfile.objects.create(user=request.user)
        
        # If user has disabled auto-detection, use their preference
        if not profile.auto_detect_timezone:
            try:
                return pytz.timezone(profile.timezone)
            except Exception:
                return None
        
        # Auto-detect from IP
        try:
            client_ip = get_client_ip(request)
            detected_tz = get_timezone_from_ip(client_ip)
            
            if detected_tz:
                # Update user profile with detected timezone
                profile.timezone = str(detected_tz)
                profile.save(update_fields=['timezone'])
                return detected_tz
            else:
                # Fallback to user's saved timezone
                return pytz.timezone(profile.timezone)
        except Exception as e:
            logger.debug(f"Error auto-detecting timezone: {e}")
            try:
                return pytz.timezone(profile.timezone)
            except Exception:
                return None
