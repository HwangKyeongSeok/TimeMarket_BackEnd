import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, ChatMessage
from users.models import User
from asgiref.sync import sync_to_async
# ✅ serializers를 import하여 데이터 형식을 통일합니다.
from .serializers import ChatMessageSerializer


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

        receiver = await self.get_receiver()

        if not receiver:
            print("🚨 상대방을 찾을 수 없어 메시지를 저장하지 않습니다.")
            return

        # ✅ DB에 메시지를 저장하고, 저장된 객체를 받아옵니다.
        new_message_obj = await self.save_message(
            self.room_name,
            self.user,
            receiver,
            message
        )

        # ✅ Serializer를 사용해 new_message_obj를 JSON으로 변환합니다.
        #    이렇게 하면 모든 데이터 타입(id는 int, 나머지는 string 등)이 정확해집니다.
        serialized_message = await self.serialize_message(new_message_obj)

        # 그룹 전체로 직렬화된 메시지 데이터를 전송합니다.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serialized_message  # ✅ 직렬화된 데이터를 전송
            }
        )

    async def chat_message(self, event):
        # ✅ 받은 데이터를 그대로 클라이언트에게 전송합니다.
        await self.send(text_data=json.dumps(event['message']))

    @sync_to_async
    def save_message(self, room_id, sender, receiver, message):
        room = Room.objects.get(id=int(room_id))
        # ✅ create()는 생성된 객체를 반환합니다.
        return ChatMessage.objects.create(room=room, sender=sender, receiver=receiver, message=message)

    @sync_to_async
    def get_receiver(self):
        room = Room.objects.get(id=int(self.room_name))
        receiver = room.users.exclude(id=self.user.id).first()
        return receiver

    # ✅ 메시지 객체를 직렬화하는 헬퍼 함수 추가
    @sync_to_async
    def serialize_message(self, message_obj):
        return ChatMessageSerializer(message_obj).data