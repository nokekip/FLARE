import os
import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timesince import timesince
from django.utils.timezone import localtime, now

from .models import Forum, Message, Media


# handle the WebSocket connections.
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.forum_id = self.scope['url_route']['kwargs']['forum_id']
        self.forum_group_name = f'forum_{self.forum_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.forum_group_name,
            self.channel_name
        )

        await self.accept()

    # Leave room group
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.forum_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        message = data['message']
        media_url = data['media_url']

        media = None
        if media_url:
            media = await self.get_or_create_media(media_url)

        forum = await self.get_forum(self.forum_id)

        new_message = await self.create_message(forum, user, message, media)
        created_at = timesince(localtime(new_message.created_at), now())

        # Send message to room group
        await self.channel_layer.group_send(
            self.forum_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'media_url': media_url,
                'sender': user.username,
                'created_at': created_at
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        media_url = event.get('media_url', '')
        sender = event['sender']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'media_url': media_url,
            'sender': sender,
            'created_at': created_at,
        }))

    # fetch forum from the database
    @database_sync_to_async
    def get_forum(self, forum_id):
        return Forum.objects.get(id=forum_id)
    
    # fetch or create media from the database
    @database_sync_to_async
    def get_or_create_media(self, media_url):
        relative_path = os.path.relpath(media_url, settings.MEDIA_URL)
        media, created = Media.objects.get_or_create(file=relative_path)
        return media
    
    # create messages
    @database_sync_to_async
    def create_message(self, forum, user, message, media):
        forum.members.add(user)
        return Message.objects.create(
            forum=forum,
            sender=user,
            text=message,
            media=media
        )