from django.urls import path
from . import views

urlpatterns = [
    path('match/request/', views.MatchRequestView.as_view(), name='match-request'), #채팅방 생성
    path('match/my-chats/', views.MyChatsView.as_view(), name='my-chats'), #내 채팅방 목록
    path('match/chat/<int:room_id>/', views.ChatRoomDetailView.as_view(), name='chat-room-detail'), #채팅방 상세
    path('match/chat/<int:room_id>/messages/', views.ChatMessageListCreateView.as_view(), name='chat-messages'), #채팅 메시지 목록(읽기 전용)
]
