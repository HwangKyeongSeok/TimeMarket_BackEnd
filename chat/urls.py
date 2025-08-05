from django.urls import path
from . import views

urlpatterns = [
    path('match/request/', views.MatchRequestView.as_view(), name='match-request'),
    path('match/my-chats/', views.MyChatsView.as_view(), name='my-chats'),
    path('match/chat/<int:room_id>/', views.ChatRoomDetailView.as_view(), name='chat-room-detail'),
]

