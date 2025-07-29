from rest_framework import serializers
from .models import TimePost

class TimePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePost
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user']
