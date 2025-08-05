from django.db import models
from posts.models import TimePost
from users.models import User

class Room(models.Model):
    post = models.ForeignKey(TimePost, on_delete=models.CASCADE, null=True, blank=True, related_name="rooms")
    users = models.ManyToManyField(User, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}"


class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message[:20]}"

