from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar, name='calendar'),
    path('messages/', views.messages_view, name='messages'),
    path('settings/', views.settings_view, name='settings'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
