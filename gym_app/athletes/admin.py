from django.contrib import admin
from gym_app.athletes.models import Athlete

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username',)
    list_filter = ('birth_date',)
