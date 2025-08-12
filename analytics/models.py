from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in seconds")

    def __str__(self):
        return self.title


class WatchSession(models.Model):
    DEVICE_CHOICES = (
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('web', 'Web'),
        ('tv', 'TV'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session_duration = models.PositiveIntegerField(blank=True, null=True, help_text="seconds")
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_rewatch = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.session_duration = int(delta.total_seconds())
        if not self.pk:
            self.is_rewatch = WatchSession.objects.filter(user=self.user, video=self.video).exists()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.video} - {self.start_time}"

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['user']),
            models.Index(fields=['video']),
        ]
