from django.contrib import admin
from .models import Activity
from django.utils.html import format_html

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'image_preview')
    search_fields = ('name', 'coach__username')
    list_filter = ('coach',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.image.url)
        return "Sin imagen"
    image_preview.short_description = "Imagen"
