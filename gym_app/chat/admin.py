from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')
    search_fields = ('sender__username', 'content')
    list_filter = ('timestamp',)
