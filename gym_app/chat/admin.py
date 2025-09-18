from django.contrib import admin
from .models import ChatMessage, ChatGroup

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'role', 'timestamp', 'flagged')
    search_fields = ('user__username', 'message')
    list_filter = ('role', 'flagged', 'timestamp')

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('members',)
