from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    pass  # o elimina la clase si no necesitas personalización

admin.site.register(User, UserAdmin)
