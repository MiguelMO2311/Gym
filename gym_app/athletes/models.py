from django.db import models
from django.conf import settings  # ✅
from gym_app.activities.models import Activity

class Athlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅
    enrolled_activities = models.ManyToManyField(Activity, related_name='athletes', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='athletes/', blank=True, null=True)

    def __str__(self):
        return self.user.username
