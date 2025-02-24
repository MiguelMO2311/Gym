# gym_app/coaches/views.py
# gym_app/coaches/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'coaches/home.html')
