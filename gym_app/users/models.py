from django.db import models
from django.contrib.auth.models import AbstractUser


# Usuario personalizado
class User(AbstractUser):
    USER_TYPES = (
        ('coach', 'Coach'),
        ('athlete', 'Athlete'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # # Relación con actividades (como participante)
    # activities = models.ManyToManyField('activities.Activity', related_name='participants', blank=True)


    def __str__(self):
        return self.username

# Perfil de Coach
class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Coach: {self.user.username}"

# Perfil de Atleta
class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.TextField(blank=True)
    level = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Athlete: {self.user.username}"

# Actividad
class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateTimeField()

    # Relación con user
    coach = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'coach'})


    # Relación con atletas
    athletes = models.ManyToManyField(User, related_name='enrolled_activities', limit_choices_to={'user_type': 'athlete'}, blank=True)

    def __str__(self):
        return self.name
