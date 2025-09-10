from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from .models import Activity
from gym_app.athletes.models import Athlete
from .forms import ActivityForm 

# Vista para listar todas las actividades
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'activities/list.html', {'activities': activities})

# Vista para mostrar el detalle de una actividad
def activity_detail(request, id):
    activity = get_object_or_404(Activity, id=id)
    athletes = activity.athletes.all()  # si tienes ManyToMany en el modelo
    return render(request, 'activities/detail.html', {
        'activity': activity,
        'athletes': athletes
    })
def activity_edit(request, id):
    activity = get_object_or_404(Activity, id=id)

    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_detail', id=activity.id)
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'activities/edit.html', {
        'form': form,
        'activity': activity
    })
