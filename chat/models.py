from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.participants.count() > 2:
            raise ValueError("A thread can't have more than 2 participants.")

    def __str__(self):
        return f"Thread {self.id} between {', '.join([p.username for p in self.participants.all()])}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username}: {self.text[:20]}"
