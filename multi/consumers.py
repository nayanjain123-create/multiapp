import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User

from .models import (
    Message,
    Room,
    ProductRoom,
    ProductMessage
)


# =========================================
# NORMAL USER CHAT
# =========================================

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        self.room_group_name = f"chat_{self.room_id}"

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

        message = data["message"]
        
        receiver_id = data["receiver_id"]

        sender = self.scope["user"]
        username = sender.username
        receiver = await sync_to_async(User.objects.get)(
            id=receiver_id
        )

        room = await sync_to_async(Room.objects.get)(
            id=self.room_id
        )

        # SAVE MESSAGE
        await sync_to_async(Message.objects.create)(
            room=room,
            sender=sender,
            receiver=receiver,
            text=message
        )

        # SEND MESSAGE TO GROUP
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))


# =========================================
# PRODUCT CHAT
# =========================================

class ProductChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.chat_id = self.scope["url_route"]["kwargs"]["room_id"]

        self.room_group_name = f"product_chat_{self.chat_id}"

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

        message = data["message"]
        username = data["username"]

        sender = self.scope["user"]

        # GET PRODUCT ROOM
        room = await sync_to_async(ProductRoom.objects.get)(
            id=self.chat_id
        )

        # SAVE PRODUCT MESSAGE
        await sync_to_async(ProductMessage.objects.create)(
            room=room,
            sender=sender,
            text=message
        )

        # SEND MESSAGE TO GROUP
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "product_message",
                "message": message,
                "username": username,
            }
        )

    async def product_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))