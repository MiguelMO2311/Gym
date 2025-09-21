# gym_app/chat/urls.py
from django.urls import path
from .views import dashboard_view, moderation_view, home


urlpatterns = [
    path('', home, name='chat_home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('moderation/', moderation_view, name='moderation'),
]

