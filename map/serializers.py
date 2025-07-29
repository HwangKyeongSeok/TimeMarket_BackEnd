from rest_framework import serializers
from .models import TimeMarker

class TimeMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeMarker
        fields = '__all__'
