from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CoachProfileForm, AthleteProfileForm
from .models import User, CoachProfile, AthleteProfile
from gym_app.coaches.models import Coach  # ✅
from gym_app.activities.models import Activity
from django.utils.html import format_html

# Import Coach model for use in profile and coach_panel views

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('users:users_home')

def users_home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        print("Datos recibidos:", request.POST)

        user_form = CustomUserCreationForm(request.POST, request.FILES)
        user_type = request.POST.get('user_type')

        coach_form = CoachProfileForm(request.POST) if user_type == 'coach' else CoachProfileForm()
        athlete_form = AthleteProfileForm(request.POST) if user_type == 'athlete' else AthleteProfileForm()

        if not user_type:
            messages.error(request, "Debes seleccionar un tipo de usuario.")
        elif user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = user_type
            user.profile_image = user_form.cleaned_data.get('profile_image')
            user.save()

            if user_type == 'coach' and coach_form.is_valid():
                coach = coach_form.save(commit=False)
                coach.user = user
                coach.save()
            elif user_type == 'athlete' and athlete_form.is_valid():
                athlete = athlete_form.save(commit=False)
                athlete.user = user
                athlete.save()

            messages.success(request, "Registro completado correctamente. ¡Bienvenido!")
            return redirect('users:users_home')
        else:
            messages.error(request, "Hubo errores en el formulario. Por favor revisa los campos.")
    else:
        user_form = CustomUserCreationForm()
        coach_form = CoachProfileForm()
        athlete_form = AthleteProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'coach_form': coach_form,
        'athlete_form': athlete_form
    })

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Mensaje personalizado
            if user.user_type == 'coach':
                messages.success(request, "Has iniciado sesión como entrenador.")
                return redirect('coach_home')  # o 'coach_panel'
            elif user.user_type == 'athlete':
                messages.success(request, "Has iniciado sesión como atleta.")
                return redirect('athlete_home')  # o 'athlete_panel'
            else:
                messages.success(request, "Has iniciado sesión correctamente.")
                return redirect('users:profile')
        else:
            messages.error(request, "Credenciales inválidas. Inténtalo de nuevo.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    is_editing = request.GET.get('edit') == 'true' or request.method == 'POST'

    # Inicialización
    profile_instance = None
    form_class = None
    related_athletes = None
    related_coaches = None

    # Lógica por tipo de usuario
    if user.user_type == 'coach':
        profile_instance = get_object_or_404(CoachProfile, user=user)
        form_class = CoachProfileForm

        try:
            coach_instance = Coach.objects.get(user=user)
            related_athletes = Activity.objects.filter(coach=coach_instance).values_list(
                'athletes__username', flat=True
            ).distinct()
        except Coach.DoesNotExist:
            related_athletes = []

    elif user.user_type == 'athlete':
        profile_instance = get_object_or_404(AthleteProfile, user=user)
        form_class = AthleteProfileForm

        related_coaches = user.enrolled_activities.values_list(
            'coach__user__username', flat=True
        ).distinct()

    # Procesamiento del formulario
    if request.method == 'POST':
        form = form_class(request.POST, instance=profile_instance)
        form.fields.pop('activities', None)  # 🔧 eliminar campo manualmente si está presente

        if form.is_valid():
            form.save()

            selected_raw = request.POST.getlist('activities')
            print("🟡 Actividades recibidas (raw):", selected_raw)

            try:
                selected_ids = []
                for item in selected_raw:
                    print("🔍 Tipo:", type(item), "| Valor:", item)
                    try:
                        selected_ids.append(int(item))
                    except (ValueError, TypeError):
                        print("❌ Valor no convertible a entero:", item)
                        continue

                print("✅ IDs válidos:", selected_ids)
                valid_activities = Activity.objects.filter(id__in=selected_ids)

                if user.user_type == 'athlete':
                    user.enrolled_activities.set(valid_activities)

                elif user.user_type == 'coach':
                    try:
                        coach_instance = Coach.objects.get(user=user)
                        for activity in valid_activities:
                            activity.coach = coach_instance
                            activity.save()
                    except Coach.DoesNotExist:
                        messages.error(request, "No se encontró el perfil de entrenador para asignar actividades.")

                messages.success(request, "Actividades actualizadas correctamente.")
                return redirect('users:profile')

            except Exception as e:
                messages.error(request, format_html(
                    "<span class='text-light'>Error al procesar las actividades seleccionadas: {}</span>", e
                ))
        else:
            messages.error(request, "Hubo errores en el formulario. Por favor revisa los campos.")
    else:
        form = form_class(instance=profile_instance)

    context = {
        'form': form,
        'is_editing': is_editing,
        'activities': Activity.objects.all(),
        'related_athletes': related_athletes,
        'related_coaches': related_coaches,
        'user': user,  # ✅ Añadir esto
    }

    return render(request, 'users/profile.html', context)

@login_required
def delete_profile(request):
    user = request.user

    if user.user_type == 'athlete':
        user.enrolled_activities.clear()
        AthleteProfile.objects.filter(user=user).delete()
    elif user.user_type == 'coach':
        Activity.objects.filter(coach=user).update(coach=None)
        CoachProfile.objects.filter(user=user).delete()

    user.delete()
    messages.success(request, "Tu cuenta ha sido eliminada correctamente.")
    return redirect('users:users_home')

@login_required
def athlete_panel(request):
    user = request.user

    if user.user_type != 'athlete':
        return redirect('coach_home')  # redirige si no es atleta

    athlete_profile = AthleteProfile.objects.filter(user=user).first()
    activities = user.enrolled_activities.all()
    coaches = activities.values_list('coach__user__username', flat=True).distinct()


    return render(request, 'athletes/home.html', {
        'athlete_profile': athlete_profile,
        'activities': activities,
        'coaches': coaches,
    })

@login_required
def coach_panel(request):
    user = request.user

    # Redirige si el usuario no es tipo coach
    if user.user_type != 'coach':
        return redirect('athlete_home')

    # Obtener perfil del coach
    coach_profile = CoachProfile.objects.filter(user=user).first()

    # Obtener instancia del modelo Coach
    try:
        coach_instance = Coach.objects.get(user=user)
    except Coach.DoesNotExist:
        coach_instance = None

    # Obtener actividades y atletas relacionados
    if coach_instance:
        activities = Activity.objects.filter(coach=coach_instance)
        athletes = activities.values_list('athletes__username', flat=True).distinct()
    else:
        activities = Activity.objects.none()
        athletes = []

    return render(request, 'coaches/home.html', {
        'coach_profile': coach_profile,
        'activities': activities,
        'athletes': athletes,
    })