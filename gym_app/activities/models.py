from django.db import models
from gym_app.coaches.models import Coach

DAYS_OF_WEEK = [
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('X', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
    ('S', 'Sábado'),
    ('D', 'Domingo'),
]

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, default='L')
    start_time = models.TimeField(default='17:00')
    end_time = models.TimeField(default='18:00')
    athletes = models.ManyToManyField('athletes.Athlete', related_name='enrolled_activities', blank=True)

    def __str__(self):
        return self.name
