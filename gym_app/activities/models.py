from django.db import models
from gym_app.coaches.models import Coach

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
