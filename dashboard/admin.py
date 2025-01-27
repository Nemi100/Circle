from django.contrib import admin
from .models import Job, Review, PreviousWork

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'project_title', 'project_description', 'project_budget', 'deadline')
    search_fields = ('project_title', 'project_description', 'client__user__username')

admin.site.register(Review)
admin.site.register(PreviousWork)
