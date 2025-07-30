from rest_framework import serializers
from .models import TimePost
# posts/serializers.py
from users.serializers import UserSerializer


class TimePostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # user 정보를 포함
    class Meta:
        model = TimePost
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user']
