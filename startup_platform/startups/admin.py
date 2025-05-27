from django.contrib import admin
from .models import Startup

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'stage', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'industry', 'stage', 'created_at']
    search_fields = ['name', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo', 'industry', 'stage')
        }),
        ('Contact Information', {
            'fields': ('location', 'website', 'email', 'phone')
        }),
        ('Status', {
            'fields': ('status', 'created_by', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        }),
    )