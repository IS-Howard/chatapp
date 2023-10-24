# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import ChatRoomMembership, ChatRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Record user in chat room
        user = self.scope["user"]
        if user.is_authenticated:
            ChatRoom.objects.get_or_create(name=self.room_name)
            ChatRoomMembership.objects.get_or_create(user=user, chat_room=self.room_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

         # Remove user from chat room
        user = self.scope["user"]
        if user.is_authenticated:
            chat_room = ChatRoom.objects.get(name=self.room_name)
            ChatRoomMembership.objects.filter(user=user, chat_room=self.room_name).delete()

        # if the chat room has no more members => delete chat room
        if not ChatRoomMembership.objects.filter(chat_room=self.room_name).exists():
            chat_room.delete() 

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"].username

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message, "username": username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "username": username}))