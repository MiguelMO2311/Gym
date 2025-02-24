# gym_app/athletes/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'athletes/home.html')
