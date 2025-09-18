# gym_app/chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage, ChatGroup
from django.db.models import Count
from django.contrib.auth.models import User

# gym_app/chat/views.py
@login_required
def chat_view(request):
    groups = ChatGroup.objects.filter(members=request.user)
    coaches = User.objects.filter(groups__name='Coaches')
    return render(request, 'athletes/home.html', {'groups': groups, 'coaches': coaches})

@login_required
def dashboard_view(request):
    stats = ChatMessage.objects.values('user__username').annotate(total=Count('id')).order_by('-total')
    return render(request, 'chat/dashboard.html', {'stats': stats})

@login_required
def moderation_view(request):
    flagged = ChatMessage.objects.filter(flagged=True).order_by('-timestamp')
    return render(request, 'chat/moderation.html', {'flagged': flagged})

def home(request):
    return render(request, 'chat/home.html')
