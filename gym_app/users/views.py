from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CoachProfileForm, AthleteProfileForm
from .models import User, CoachProfile, AthleteProfile

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('users:users_home')


def users_home(request):
    return render(request, 'users/home.html')



def register(request):
    if request.method == 'POST':
        print("Datos recibidos:", request.POST)  # 👈 Esto te mostrará los datos en consola

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
            return redirect('users_home')
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

    if user.user_type == 'coach':
        profile_instance = get_object_or_404(CoachProfile, user=user)
        form_class = CoachProfileForm
        related_athletes = AthleteProfile.objects.filter(user__activities__coach=user).distinct()
        activities = user.activities.all()
    else:
        profile_instance = get_object_or_404(AthleteProfile, user=user)
        form_class = AthleteProfileForm
        related_coaches = CoachProfile.objects.filter(user__activities__athletes=user).distinct()
        activities = user.activities.all()

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
    else:
        form = form_class(instance=profile_instance)

    context = {
        'form': form,
        'is_editing': is_editing,
        'activities': activities,
        'related_athletes': related_athletes if user.user_type == 'coach' else None,
        'related_coaches': related_coaches if user.user_type == 'athlete' else None,
    }

    return render(request, 'users/profile.html', context)

@login_required
def delete_profile(request):
    user = request.user

    if user.user_type == 'coach':
        CoachProfile.objects.filter(user=user).delete()
    elif user.user_type == 'athlete':
        AthleteProfile.objects.filter(user=user).delete()

    user.delete()
    messages.success(request, "Tu cuenta ha sido eliminada correctamente.")
    return redirect('users_home')
