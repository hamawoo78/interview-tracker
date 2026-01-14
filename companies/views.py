from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Company
from .forms import CompanyForm
from interviews.models import InterviewEvent
from prep.models import InterviewPrep
from core.openai_service import extract_company_details
import json
from django.http import JsonResponse


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20

    def get_queryset(self):
        queryset = Company.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        location = self.request.GET.get('location')
        
        if status:
            queryset = queryset.filter(status=status)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Company.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_location'] = self.request.GET.get('location', '')
        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['interviews'] = company.interviews.all()
        context['prep'] = InterviewPrep.objects.filter(company=company).first()
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('company_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Company '{self.object.name}' created successfully!")
        return response


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('company_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Company '{self.object.name}' updated successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk})


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'companies/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')

    def delete(self, request, *args, **kwargs):
        company_name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Company '{company_name}' deleted successfully!")
        return response

#  do we need this?
@login_required
def company_list_api(request):
    """API endpoint for company list (for sidebar dropdown)."""
    companies = Company.objects.filter(user=request.user).values('id', 'name')
    return render(request, 'companies/company_list_dropdown.html', {'companies': companies})



@login_required
@require_http_methods(["POST"])
def extract_company_info_email(request):
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
        extracted_data = extract_company_details(email_text)
        
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
