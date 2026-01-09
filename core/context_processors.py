from companies.models import Company


def all_companies(request):
    """Add all companies to template context for sidebar."""
    if request.user.is_authenticated:
        companies = Company.objects.all()[:20]  # Limit to 20 for sidebar
    else:
        companies = []
    return {'all_companies': companies}
