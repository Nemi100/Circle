from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'budget', 'deadline']
    search_fields = ['title', 'description']
    list_filter = ['deadline', 'budget', 'skills_required']