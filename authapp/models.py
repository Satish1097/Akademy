from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, blank=True)
    mobile = models.CharField(max_length=13, null=True, blank=True)
    profile_picture = models.ImageField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("organizer", "Organizer"),
        ("user", "User"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    date_joined = models.DateTimeField(default=timezone.now)

    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class OTP(models.Model):
    mobile = models.CharField(max_length=13, blank=True)
    email = models.EmailField(blank=True)
    secret_key = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        info = self.email if self.email else self.mobile
        return f"OTP for {info}"


class UserToken(models.Model):
    refresh_token = models.CharField(
        max_length=255, unique=True
    )  # Unique device identifier
    access_token = models.CharField(max_length=255, unique=True)


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="images/company_logos/", null=True, blank=True)
    address = models.TextField()
    breaf_desc_of_company = models.TextField()

    def __str__(self):
        return self.company_name


class BankAccount(models.Model):
    organizer = models.OneToOneField(Organizer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.organizer.user.username} - {self.account_number}"


class EventCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    banner = models.ImageField(upload_to="images/event_banners/")
    description = models.TextField()
    speaker = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(
        max_length=50, choices=[("Online", "Online"), ("Offline", "Offline")]
    )
    venue = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.PositiveIntegerField()
    schedule = models.DateTimeField()
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_events"
    )
    categories = models.ManyToManyField(EventCategory, related_name="events")

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    medical_score = models.IntegerField(default=0)
    language_choice = [("en", "English"), ("ar", "Arabic")]
    prefered_language = models.CharField(
        max_length=10, choices=language_choice, default="en"
    )

    def __str__(self):
        return f"{self.user.email}'s Profile"


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


class Registration(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    refund_initiated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("Event Update", "Event Update"),
        ("Organizer Message", "Organizer Message"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"


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
