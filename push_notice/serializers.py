from rest_framework import serializers
from .models import DeviceToken

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["token", "platform"]

    def create(self, validated_data):
        user = self.context["request"].user
        token = validated_data["token"]
        platform = validated_data.get("platform", "android")
        obj, _ = DeviceToken.objects.update_or_create(
            token=token,
            defaults={"user": user, "platform": platform, "is_active": True},
        )
        return obj

