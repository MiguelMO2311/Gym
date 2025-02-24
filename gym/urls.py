
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gym_app import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activities/', include('gym_app.activities.urls')),
    path('coaches/', include('gym_app.coaches.urls')),  # Incluir las URLs de coaches
    path('athletes/', include('gym_app.athletes.urls')),
    path('chat/', include('gym_app.chat.urls')),  # Incluir las URLs de chat
    path('users/', include('gym_app.users.urls')),
    path('', views.home, name='home'), 
    path('', include('gym_app.urls')),
]

# Añadir rutas para servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)