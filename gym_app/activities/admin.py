from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach')
    search_fields = ('name', 'coach__user__username')
    list_filter = ('coach',)
