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


class OrganizerSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Organizer
        fields = [
            "user",
            "user_id",
            "company_name",
            "logo",
            "address",
            "breaf_desc_of_company",
        ]


class BankSerializer(serializers.ModelSerializer):
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizer.objects.all(), write_only=True
    )
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = [
            "organizer",
            "organizer_id",
            "account_number",
            "bank_name",
            "ifsc_code",
        ]
