from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:company_id>/', views.InterviewEventCreateView.as_view(), name='interview_create'),
    path('<int:pk>/edit/', views.InterviewEventUpdateView.as_view(), name='interview_edit'),
    path('<int:pk>/delete/', views.InterviewEventDeleteView.as_view(), name='interview_delete'),
    path('api/extract-email/', views.extract_interview_email, name='extract_interview_email'),
]
