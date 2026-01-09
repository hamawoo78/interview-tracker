from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar, name='calendar'),
    path('messages/', views.messages, name='messages'),
    path('settings/', views.settings_view, name='settings'),
]
