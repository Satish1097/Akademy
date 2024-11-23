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


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     medical_score = models.IntegerField(default=0)
#     language_choice = [("en", "English"), ("ar", "Arabic")]
#     prefered_language = models.CharField(
#         max_length=10, choices=language_choice, default="en"
#     )

#     def __str__(self):
#         return f"{self.user.email}'s Profile"
