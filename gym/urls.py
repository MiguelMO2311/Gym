# gym/urls.py
from django.contrib import admin
from django.urls import path, include
from gym_app import views  # Importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activities/', include('gym_app.activities.urls')),
    path('coaches/', include('gym_app.coaches.urls')),  # Incluir las URLs de coaches
    path('athletes/', include('gym_app.athletes.urls')),
    path('chat/', include('gym_app.chat.urls')),  # Incluir las URLs de chat
    path('users/', include('gym_app.users.urls')),
    path('', views.home, name='home'),  # Agregar la URL de la página de inicio
]
