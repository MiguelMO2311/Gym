from django.db import models
from django.conf import settings  # ✅


class Coach(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅
    bio = models.TextField(blank=True)
    specialty = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='coaches/', blank=True, null=True)

    def __str__(self):
        return self.user.username

