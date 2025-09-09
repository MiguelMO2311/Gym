from django.contrib import admin
from .models import Coach

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'phone')
    search_fields = ('user__username', 'specialty')
