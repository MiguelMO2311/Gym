from django.db import models

class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('users.User')  # ← referencia segura por string

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'Usuario'),
        ('ai', 'IA'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)  # ← también por string
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ({self.role}): {self.message[:30]}"
