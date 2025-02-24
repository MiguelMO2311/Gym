# gym_app/activities/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='activities_home'),
]
