from django.db import models
from authapp.models import User
from events.models import Event

# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("Event Update", "Event Update"),
        ("Organizer Message", "Organizer Message"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"
