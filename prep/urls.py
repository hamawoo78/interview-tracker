from django.urls import path
from . import views

urlpatterns = [
    path('<int:company_id>/edit/', views.prep_edit, name='prep_edit'),
]
