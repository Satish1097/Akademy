from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from authapp.models import *
from authapp.models import OTP
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from datetime import datetime


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "mobile", "username", "role"]

    def validate(self, attrs):
        # Ensure the passwords match
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")  # Remove password2 field
        user = User.objects.create(
            email=validated_data["email"],
            mobile=validated_data.get("mobile"),
            username=validated_data.get("username", ""),
            role=validated_data.get("role"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Only validate that mobile or email is provided
        mobile = attrs.get("mobile", None)
        email = attrs.get("email", None)

        if not (mobile or email):
            raise serializers.ValidationError(
                "Please provide either a mobile number or an email address."
            )

        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate_schedule(self, sheduled_date):
        if sheduled_date <= datetime.now():
            raise ValidationError("The event schedule must be in the future.")
        return sheduled_date


class SavedEventSerializer(serializers.ModelSerializer):
    class Meta:
        models = SavedEvent
        fields = ["user", "event"]

    def validate(self, data):
        user = data["user"]
        event = data["event"]
        if SavedEvent.objects.filter(user=user, event=event).exists():
            raise ValidationError("You have already saved this event.")
        return data


class CertificateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        models = CertificateIssue
        fields = ["certificate", "user", "issue_description", "resolved", "created_at"]
