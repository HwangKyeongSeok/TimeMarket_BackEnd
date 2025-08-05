import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, ChatMessage
from users.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']
        print("📨 WebSocket message received")
        print("  From:", self.user.id, self.user.nickname)
        print("  To:", data.get("receiver_id"))
        print("  Room:", self.room_name)
        print("  Message:", data.get("message"))
        # DB 저장
        await self.save_message(
            self.room_name,
            self.user.id,
            receiver_id,
            message
        )

        # 그룹 전체로 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.nickname  # 사용자 닉네임 표시
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @sync_to_async
    def save_message(self, room_id, sender_id, receiver_id, message):
        room = Room.objects.get(id=int(room_id))
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        ChatMessage.objects.create(room=room, sender=sender, receiver=receiver, message=message)
