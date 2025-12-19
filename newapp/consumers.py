# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        print("web sockets now are in tje data connects",self.user)
        if self.user.is_anonymous:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"✅ Connected to WebSocket room: {self.room_name}")
        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))

    async def disconnect(self, close_code):
       await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data.get('message')   
        print(message)                                                                                    
        await self.save_message(self.user, self.room_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'message': message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'sender': event['sender'],
            'message': event['message'],
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, message):
        room = Room.objects.get(name=room_name)
        Message.objects.create(room=room, user=user, content=message)

    @database_sync_to_async
    def get_messages(self):
        room = Room.objects.get(name=self.room_name)
        print( "room ides",room)
        messages = Message.objects.filter(room=room).select_related('user').order_by('timestamp')
        print(messages)
        return [
            {
                'sender': msg.user.username,
                'message': msg.content,
                'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for msg in messages
        ]
