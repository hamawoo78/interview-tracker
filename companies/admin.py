from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'position_title', 'location', 'status', 'updated_at')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('name', 'position_title', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'logo', 'website_url', 'location')
        }),
        ('Position', {
            'fields': ('position_title', 'salary_min', 'salary_max')
        }),
        ('Job Description', {
            'fields': ('job_description_url', 'job_description_file')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
