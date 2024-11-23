from rest_framework import serializers
from payments.models import *


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PayoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = "__all__"
