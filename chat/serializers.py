from rest_framework import serializers
from .models import ChatMessage, Room
from users.models import User

# ✅ 채팅방 목록과 메시지에 필요한 최소한의 유저 정보를 담을 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_image']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'receiver', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'sender', 'receiver', 'room']

# ✅ 1. 기본 채팅방 정보를 위한 RoomSerializer를 다시 정의합니다.
#    MatchRequestView와 ChatRoomDetailView에서 사용됩니다.
class RoomSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ['id', 'post', 'users', 'created_at']

# ✅ 2. 채팅방 '목록'에 필요한 상세 정보를 담는 ChatRoomListSerializer는 그대로 유지합니다.
#    MyChatsView에서 사용됩니다.
class ChatRoomListSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'post', 'other_user', 'last_message', 'created_at']

    def get_other_user(self, obj):
        user = self.context['request'].user
        other_user = obj.users.exclude(id=user.id).first()
        return UserSerializer(other_user, context=self.context).data if other_user else None

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        return ChatMessageSerializer(last_msg, context=self.context).data if last_msg else None