from django.db import models
from django.conf import settings  # ✅

class Athlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='athletes/', blank=True, null=True)

    def __str__(self):
        return self.user.username
