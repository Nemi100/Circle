from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'recipient__username', 'subject')