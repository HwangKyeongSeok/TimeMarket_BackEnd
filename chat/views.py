from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Room, ChatMessage
from .serializers import RoomSerializer, ChatMessageSerializer
from users.models import User
from posts.models import TimePost
from django.http import Http404
from push_notice.services import send_push_to_user  # 추가

class MatchRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        receiver_id = request.data.get('receiver_id')

        try:
            post = TimePost.objects.get(id=post_id)
        except TimePost.DoesNotExist:
            raise Http404("TimePost with the given ID does not exist.")

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise Http404("User with the given ID does not exist.")

        room = Room.objects.create(post=post)
        room.users.add(request.user, receiver)

        # 방 생성 알림 전송 (수신자에게)
        try:
            title = f"{request.user.nickname}와 새로운 채팅방"
            body = f"게시글: {post.title}"
            data = {"type": "room_created", "room_id": str(room.id), "post_id": str(post.id)}
            send_push_to_user(receiver, title, body, data)
        except Exception:
            pass

        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

class MyChatsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    def get_queryset(self):
        return Room.objects.filter(users=self.request.user)

class ChatRoomDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'room_id'

class ChatMessageListCreateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer
    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.filter(room_id=room_id).order_by('timestamp')
