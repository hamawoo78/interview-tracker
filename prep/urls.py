from django.urls import path
from . import views

urlpatterns = [
    path('<int:company_id>/edit/', views.prep_edit, name='prep_edit'),
    path('api/rate/', views.rate_prep_api, name='rate_prep_api'),
]
