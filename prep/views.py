from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from companies.models import Company
from .models import InterviewPrep
from .forms import InterviewPrepForm
from core.openai_service import rate_prep_answers


@login_required
def prep_edit(request, company_id):
    """Edit interview prep notes for a company."""
    company = get_object_or_404(Company, pk=company_id)
    prep, created = InterviewPrep.objects.get_or_create(company=company)
    
    if request.method == 'POST':
        form = InterviewPrepForm(request.POST, instance=prep)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview prep notes saved successfully!")
            return redirect('company_detail', pk=company.pk)
    else:
        form = InterviewPrepForm(instance=prep)
    
    context = {
        'form': form,
        'company': company,
        'prep': prep,
    }
    return render(request, 'prep/prep_form.html', context)


@login_required
@require_http_methods(["POST"])
def rate_prep_api(request):
    """
    API endpoint to rate interview prep answers using AI.
    
    Request: POST /prep/api/rate/
    Body: { "company_id": 1, "prep_answers": {...} }
    
    Response: { "ok": true, "ratings": {...} } or { "ok": false, "error": "..." }
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        company_id = data.get('company_id')
        prep_answers = data.get('prep_answers', {})
        
        # Validate input
        if not company_id:
            return JsonResponse({
                'ok': False,
                'error': 'company_id is required'
            }, status=400)
        
        # Get company and job description
        company = get_object_or_404(Company, pk=company_id)
        job_description = company.job_description_url or company.job_description_file or "No job description provided"
        
        # If job_description_file, try to get URL
        if hasattr(job_description, 'url'):
            job_description = f"Job description file: {job_description.url}"
        
        # Call OpenAI service to rate answers
        ratings = rate_prep_answers(prep_answers, job_description)
        
        # Check if rating had an error
        if 'error' in ratings:
            return JsonResponse({
                'ok': False,
                'error': ratings['error']
            }, status=400)
        
        # Return ratings
        return JsonResponse({
            'ok': True,
            'ratings': ratings
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'ok': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=500)
