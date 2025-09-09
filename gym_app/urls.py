from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('gym_app.users.urls')),
    path('athletes/', include('gym_app.athletes.urls')),
    path('coaches/', include('gym_app.coaches.urls')),
    path('activities/', include('gym_app.activities.urls')),
    path('chat/', include('gym_app.chat.urls')),
]
