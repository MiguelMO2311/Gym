from django.db import models
from django.conf import settings  # ← esto es clave

class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)  # ← corregido

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    ROLE_CHOICES = (('user', 'Usuario'), ('ai', 'IA'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ← corregido
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ({self.role}): {self.message[:30]}"
