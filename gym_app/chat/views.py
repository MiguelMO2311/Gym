# gym_app/chat/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'chat/home.html')
