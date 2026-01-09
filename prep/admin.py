from django.contrib import admin
from .models import InterviewPrep


@admin.register(InterviewPrep)
class InterviewPrepAdmin(admin.ModelAdmin):
    list_display = ('company', 'updated_at')
    search_fields = ('company__name',)
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Company', {
            'fields': ('company',)
        }),
        ('Prep Content', {
            'fields': ('self_intro', 'why_apply', 'questions_to_ask', 'additional_notes')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
