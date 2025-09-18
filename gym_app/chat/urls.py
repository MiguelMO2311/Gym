# gym_app/chat/urls.py
from django.urls import path
from . import views
from .views import chat_view, dashboard_view, moderation_view

urlpatterns = [
    path('', views.home, name='chat_home'),
    path('', chat_view, name='chat'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('moderation/', moderation_view, name='moderation'),
]
