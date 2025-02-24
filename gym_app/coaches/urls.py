# gym_app/coaches/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='coach_home'),
]
