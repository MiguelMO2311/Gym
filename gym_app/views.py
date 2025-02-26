# gym_app/views.py
from django.shortcuts import render

def base(request):
    return render(request, 'base.html')
