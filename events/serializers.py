from rest_framework import serializers
from events.models import *
from authapp.models import Organizer
from datetime import datetime
from rest_framework.exceptions import ValidationError
from authapp.serializers import OrganizerSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.all(), write_only=True
    )
    organizer = OrganizerSerializer(read_only=True)
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizer.objects.all(), write_only=True
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "event_banner",
            "description_of_event",
            "speaker_details",
            "ticket_price",
            "mode_of_event",
            "venue",
            "capacity",
            "schedule",
            "organizer",
            "organizer_id",
            "category",
            "category_id",
            "event_point",
            "status",
        ]

    def validate(self, data):
        """
        1. The venue is not blank unless the mode_of_event is 'Online'.
        2. The event's schedule is in the future.
        """
        mode_of_event = data.get("mode_of_event")
        venue = data.get("venue")
        schedule = data.get("schedule")

        if mode_of_event == "Offline" and not venue:
            raise serializers.ValidationError(
                {"venue": "Venue is required for offline events."}
            )

        if schedule and schedule <= datetime.now():
            raise serializers.ValidationError(
                {"schedule": "The event schedule must be in the future."}
            )

        return data


class SavedEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), write_only=True
    )

    class Meta:
        models = SavedEvent
        fields = ["user", "event", "event_id"]

    def validate(self, data):
        user = data["user"]
        event = data["event"]
        if SavedEvent.objects.filter(user=user, event=event).exists():
            raise ValidationError("You have already saved this event.")
        return data


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        models = Certificate
        fields = ["user", "file", "uploaded_at", "issued_at", "event"]


class CertificateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        models = CertificateIssue
        fields = ["certificate", "user", "issue_description", "resolved", "created_at"]


class EventRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        models = Registration
        fields = [
            "user",
            "event",
            "registered_at",
            "payment_status",
            "is_confirmed",
            "refund_initiated",
        ]
