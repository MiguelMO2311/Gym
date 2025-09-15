from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='coach_home'),
]
