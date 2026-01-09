from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_edit'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
    path('api/list/', views.company_list_api, name='company_list_api'),
    path('api/extract-email/', views.extract_company_info_email, name='extract_company_info_email'),

]
