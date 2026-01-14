from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from companies.models import Company
from .models import InterviewEvent
from .forms import InterviewEventForm
from core.openai_service import extract_interview_details


class InterviewEventCreateView(LoginRequiredMixin, CreateView):
    model = InterviewEvent
    form_class = InterviewEventForm
    template_name = 'interviews/interview_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.kwargs.get('company_id')
        context['company'] = get_object_or_404(Company, pk=company_id)
        return context

    def form_valid(self, form):
        company_id = self.kwargs.get('company_id')
        company = get_object_or_404(Company, pk=company_id, user=self.request.user)
        form.instance.company = company
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Interview event created successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.company.pk})



class InterviewEventUpdateView(LoginRequiredMixin, UpdateView):
    model = InterviewEvent
    form_class = InterviewEventForm
    template_name = 'interviews/interview_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.object.company.pk
        context['company'] = get_object_or_404(Company, pk=company_id)
        return context

    def form_valid(self, form):
        # print(form.cleaned_data.get('start_datetime'))
        response = super().form_valid(form)
        messages.success(self.request, "Interview event updated successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.company.pk})


class InterviewEventDeleteView(LoginRequiredMixin, DeleteView):
    model = InterviewEvent
    template_name = 'interviews/interview_confirm_delete.html'

    def get_success_url(self):
        company_id = self.object.company.pk
        messages.success(self.request, "Interview event deleted successfully!")
        return reverse_lazy('company_detail', kwargs={'pk': company_id})


@login_required
@require_http_methods(["POST"])
def extract_interview_email(request):
    """
    API endpoint to extract interview details from pasted email using OpenAI.
    
    Request: POST /interviews/api/extract-email/
    Body: { "email_text": "..." }
    
    Response: { "ok": true, "data": {...} } or { "ok": false, "error": "..." }
    
    Important: This endpoint does NOT save to database.
    It only extracts and returns data for the user to review and manually save.
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        email_text = data.get('email_text', '').strip()
        
        # Validate input
        if not email_text:
            return JsonResponse({
                'ok': False,
                'error': 'Email text is required'
            }, status=400)
        
        if len(email_text) > 10000:
            return JsonResponse({
                'ok': False,
                'error': 'Email text is too long (max 10000 characters)'
            }, status=400)
        
        # Call OpenAI service to extract details
        extracted_data = extract_interview_details(email_text)
        
        # Check if extraction had an error
        if 'error' in extracted_data:
            return JsonResponse({
                'ok': False,
                'error': extracted_data['error']
            }, status=400)
        
        # Return extracted data (user will review and submit manually)
        return JsonResponse({
            'ok': True,
            'data': extracted_data
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
