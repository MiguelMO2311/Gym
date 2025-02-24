# gym_app/activities/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'activities/home.html')
