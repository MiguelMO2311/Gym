from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('coach', 'Coach'),
        ('athlete', 'Athlete'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Añadir related_name único
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Añadir related_name único
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    experience_years = models.IntegerField()

class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    birthdate = models.DateField()
