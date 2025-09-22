from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include('gym_app.users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('athletes/', include('gym_app.athletes.urls')),
    path('coaches/', include('gym_app.coaches.urls')),
    path('activities/', include('gym_app.activities.urls')),
    path('chat/', include('gym_app.chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
