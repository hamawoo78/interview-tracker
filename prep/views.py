from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from companies.models import Company
from .models import InterviewPrep
from .forms import InterviewPrepForm


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
