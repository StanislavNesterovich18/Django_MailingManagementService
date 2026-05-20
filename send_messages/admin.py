from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_letter', 'owner', 'created_at', 'updated_at']
    list_filter = ['created_at', 'owner']
    search_fields = ['subject_letter', 'body_letter']
    readonly_fields = ['created_at', 'updated_at']
