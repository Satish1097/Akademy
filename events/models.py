from django.db import models
from authapp.models import User


class EventCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_banner = models.ImageField(upload_to="images/event_banners/")
    description_of_event = models.TextField()
    speaker_details = models.TextField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_event = models.CharField(
        max_length=50, choices=[("Online", "Online"), ("Offline", "Offline")]
    )
    venue = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.PositiveIntegerField()
    schedule = models.DateTimeField()
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_events"
    )
    categories = models.ManyToManyField(EventCategory, related_name="events")
    event_point = models.PositiveIntegerField(default=0)

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending_approval", "Pending Approval"),
        ("published", "Published"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("postponed", "Postponed"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    def __str__(self):
        return self.title


class SavedEvent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saved_events"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="saved_by")

    class Meta:
        unique_together = ("user", "event")


class Registration(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    payment_status_choice = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    payment_status = models.CharField(max_length=50, choices=payment_status_choice)
    is_confirmed = models.BooleanField(default=False)
    refund_initiated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"


class Certificate(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certificates"
    )
    file = models.FileField(upload_to="certificates/")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    issued_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Certificate for {self.user.email}"


class CertificateIssue(models.Model):
    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, related_name="issues"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certificate_issues"
    )
    issue_description = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue for {self.certificate} by {self.user.email}"
