from django.shortcuts import render, get_object_or_404
from .models import Activity
from gym_app.athletes.models import Athlete

# Vista para listar todas las actividades
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'activities/list.html', {'activities': activities})

# Vista para mostrar el detalle de una actividad
def activity_detail(request, id):
    activity = get_object_or_404(Activity, id=id)
    athletes = activity.athlete_set.all()  # si tienes ManyToMany en el modelo
    return render(request, 'activities/detail.html', {
        'activity': activity,
        'athletes': athletes
    })
