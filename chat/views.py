from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Room, ChatMessage
from .serializers import RoomSerializer, ChatMessageSerializer
from users.models import User
from posts.models import TimePost
from django.http import Http404

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

class ChatMessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer
    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.filter(room_name=str(room_id)).order_by('timestamp')
    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        receiver_id = self.request.data.get('receiver_id')
        serializer.save(
            room_name=str(room_id),
            sender=self.request.user,
            receiver=User.objects.get(id=receiver_id)
        )
