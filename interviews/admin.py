from django.contrib import admin
from .models import InterviewEvent


@admin.register(InterviewEvent)
class InterviewEventAdmin(admin.ModelAdmin):
    list_display = ('company', 'start_datetime', 'interview_type', 'interviewer_name')
    list_filter = ('interview_type', 'start_datetime', 'company')
    search_fields = ('company__name', 'interviewer_name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Interview Info', {
            'fields': ('company', 'start_datetime', 'end_datetime', 'interview_type')
        }),
        ('Interviewer', {
            'fields': ('interviewer_name', 'meeting_link')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
