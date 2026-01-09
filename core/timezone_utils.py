import pytz
import requests
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Free IP geolocation services
GEOIP_SERVICES = [
    {
        'name': 'ip-api',
        'url': 'http://ip-api.com/json/{ip}',
        'timezone_key': 'timezone',
        'rate_limit': 45,  # requests per minute
    },
    {
        'name': 'ipapi',
        'url': 'https://ipapi.co/{ip}/json/',
        'timezone_key': 'timezone',
        'rate_limit': 30,
    },
]


def get_timezone_from_ip(ip_address, use_cache=True):
    """
    Get timezone from IP address using free geolocation API.
    
    Args:
        ip_address: IP address string
        use_cache: Whether to cache results
    
    Returns:
        pytz timezone object or None
    """
    # Skip private IPs
    if is_private_ip(ip_address):
        return None
    
    # Check cache first
    if use_cache:
        cache_key = f'timezone_{ip_address}'
        cached_tz = cache.get(cache_key)
        if cached_tz:
            try:
                return pytz.timezone(cached_tz)
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    
    # Try each service
    for service in GEOIP_SERVICES:
        try:
            tz_name = fetch_timezone_from_service(ip_address, service)
            if tz_name:
                try:
                    tz = pytz.timezone(tz_name)
                    # Cache for 24 hours
                    if use_cache:
                        cache.set(f'timezone_{ip_address}', tz_name, 86400)
                    return tz
                except pytz.exceptions.UnknownTimeZoneError:
                    logger.warning(f"Unknown timezone: {tz_name}")
                    continue
        except Exception as e:
            logger.debug(f"Error with {service['name']}: {e}")
            continue
    
    return None


def fetch_timezone_from_service(ip_address, service):
    """Fetch timezone from a specific geolocation service."""
    try:
        url = service['url'].format(ip=ip_address)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        tz_name = data.get(service['timezone_key'])
        
        return tz_name
    except requests.exceptions.RequestException as e:
        logger.debug(f"Request error: {e}")
        return None
    except Exception as e:
        logger.debug(f"Error fetching timezone: {e}")
        return None


def is_private_ip(ip_address):
    """Check if IP is private/local."""
    private_ranges = [
        '127.0.0.1',
        '192.168.',
        '10.',
        '172.16.',
        'localhost',
    ]
    return any(ip_address.startswith(r) for r in private_ranges)


def get_client_ip(request):
    """
    Get client IP address from request.
    Handles proxies and load balancers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
