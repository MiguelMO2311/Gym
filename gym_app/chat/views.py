# gym_app/chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatGroup
from django.db.models import Count

# gym_app/chat/views.py

@login_required
def dashboard_view(request):
    stats = ChatMessage.objects.values('user__username').annotate(total=Count('id')).order_by('-total')
    return render(request, 'chat/dashboard.html', {'stats': stats})

@login_required
def moderation_view(request):
    flagged = ChatMessage.objects.filter(flagged=True).order_by('-timestamp')
    return render(request, 'chat/moderation.html', {'flagged': flagged})


User = get_user_model()

@login_required
def home(request):
    groups = ChatGroup.objects.filter(members=request.user)
    coaches = User.objects.filter(groups__name='Coaches')
    stats = ChatMessage.objects.values('user__username').annotate(total=Count('id')).order_by('-total')
    flagged = ChatMessage.objects.filter(flagged=True).order_by('-timestamp')

    return render(request, 'chat/home.html', {
        'groups': groups,
        'coaches': coaches,
        'stats': stats,
        'flagged': flagged,
    })
