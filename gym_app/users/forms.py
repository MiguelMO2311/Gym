from django import forms
from .models import User, CoachProfile, AthleteProfile
from django.contrib.auth.forms import UserCreationForm

# Formulario de creación de usuario
class CustomUserCreationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_image')

# Formulario de perfil de coach
class CoachProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    specialty = forms.CharField(required=False)

    class Meta:
        model = CoachProfile
        fields = ('bio', 'specialty')

# Formulario de perfil de atleta
class AthleteProfileForm(forms.ModelForm):
    goals = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    level = forms.CharField(required=False)

    class Meta:
        model = AthleteProfile
        fields = ('goals', 'level')
