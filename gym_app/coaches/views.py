from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from gym_app.users.models import CoachProfile

@login_required
def home(request):
    user = request.user

    if user.user_type != 'coach':
        return redirect('users:athlete_panel')


    coach_profile = CoachProfile.objects.filter(user=user).first()
    activities = user.enrolled_activities.all()
    athletes = activities.values_list('athletes__username', flat=True).distinct()

    return render(request, 'coaches/home.html', {
        'coach_profile': coach_profile,
        'activities': activities,
        'athletes': athletes,
    })
