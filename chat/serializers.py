from rest_framework import serializers
from .models import ChatMessage, Room
from users.models import User

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nickname")

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(write_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    room_id = serializers.IntegerField(write_only=True)
    # 조회 시 표시될 필드
    sender = UserBriefSerializer(read_only=True)
    receiver = UserBriefSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room_id', 'sender_id', 'receiver_id', 'sender', 'receiver', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'sender', 'receiver']

    def create(self, validated_data):
        sender = User.objects.get(id=validated_data.pop('sender_id'))
        receiver = User.objects.get(id=validated_data.pop('receiver_id'))
        room = Room.objects.get(id=validated_data.pop('room_id'))
        return ChatMessage.objects.create(sender=sender, receiver=receiver, room=room, **validated_data)

class RoomSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)
    class Meta:
        model = Room
        fields = ['id', 'post', 'users', 'created_at']
