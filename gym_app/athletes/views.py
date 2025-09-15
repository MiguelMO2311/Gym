from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from gym_app.users.models import AthleteProfile

@login_required
def home(request):
    user = request.user

    if user.user_type != 'athlete':
        return redirect('users:coach_panel')

    athlete_profile = AthleteProfile.objects.filter(user=user).first()
    activities = user.enrolled_activities.all()
    coaches = activities.values_list('coach__username', flat=True).distinct()

    return render(request, 'athletes/home.html', {
        'athlete_profile': athlete_profile,
        'activities': activities,
        'coaches': coaches,
    })
