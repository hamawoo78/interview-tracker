from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from companies.models import Company
from interviews.models import InterviewEvent
from django.db.models import Q
from .forms import UserProfileForm
from .models import UserProfile


@login_required
def dashboard(request):
    """Dashboard view with company cards and weekly calendar."""
    query = request.GET.get('q', '')
    
    companies = Company.objects.all()
    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(position_title__icontains=query) |
            Q(location__icontains=query)
        )
    
    # Get upcoming interviews for the next 7 days
    now = timezone.now()
    week_end = now + timedelta(days=7)
    upcoming_interviews = InterviewEvent.objects.filter(
        start_datetime__gte=now,
        start_datetime__lte=week_end
    ).order_by('start_datetime')
    
    # Group interviews by day
    interviews_by_day = {}
    for interview in upcoming_interviews:
        day = interview.start_datetime.date()
        if day not in interviews_by_day:
            interviews_by_day[day] = []
        interviews_by_day[day].append(interview)
    
    context = {
        'companies': companies,
        'query': query,
        'interviews_by_day': interviews_by_day,
        'upcoming_interviews': upcoming_interviews,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def calendar(request):
    """Calendar view showing upcoming interviews."""
    now = timezone.now()
    week_end = now + timedelta(days=7)
    upcoming_interviews = InterviewEvent.objects.filter(
        start_datetime__gte=now,
        start_datetime__lte=week_end
    ).order_by('start_datetime')
    
    # Group interviews by day
    interviews_by_day = {}
    for interview in upcoming_interviews:
        day = interview.start_datetime.date()
        if day not in interviews_by_day:
            interviews_by_day[day] = []
        interviews_by_day[day].append(interview)
    
    context = {
        'interviews_by_day': interviews_by_day,
        'upcoming_interviews': upcoming_interviews,
    }
    return render(request, 'core/calendar.html', context)


@login_required
def messages(request):
    """Messages placeholder page."""
    return render(request, 'core/messages.html')


@login_required
def settings_view(request):
    """User settings page for timezone and preferences."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'current_timezone': timezone.get_current_timezone(),
    }
    return render(request, 'core/settings.html', context)
