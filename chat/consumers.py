from django.contrib.auth import get_user_model
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from reservations.models import RoomReservation
from .serializers import MessageSerializer
from .models import Message
from .utils import parse_querystring
import json

MESSAGE_NOT_VALID_TOKEN = "this token does not match user"
MESSAGE_NOT_VALID_HOST = "this token is not host of the reservation"
MESSAGE_NOT_VALID_CLIENT = "this token is not client of the reservation"
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    reservation_id = None
    is_host = False
    group_name = None
    user = None

    @database_sync_to_async
    def _get_host(self):
        return RoomReservation.objects.get(pk=self.reservation_id).room.host

    @database_sync_to_async
    def _get_user(self, token):
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            user = None
        return user

    @database_sync_to_async
    def _get_client(self):
        try:
            client = RoomReservation.objects.get(pk=self.reservation_id).user
        except RoomReservation.DoesNotExist:
            client = None
        return client

    @database_sync_to_async
    def save(self, model_object):
        return model_object.save()

    async def _valid_client(self):
        client = await self._get_client()
        if self.user == client:
            return True
        return False

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
        await self.close()

    async def connect(self):
        self.reservation_id = self.scope['url_route']['kwargs']['pk']
        self.group_name = 'chat_%s' % self.reservation_id

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        byte_querystring = self.scope['query_string']
        query_dict = await parse_querystring(byte_querystring)
        token = query_dict.get('token')
        self.user = await self._get_user(token)

        if self.user is None:
            return await self.send_error(MESSAGE_NOT_VALID_TOKEN)

        if query_dict.get('user_type') == 'host':
            host = await self._get_host()
            if self.user != host:
                return await self.send_error(MESSAGE_NOT_VALID_HOST)
            self.is_host = True
            return

        if not await self._valid_client():
            return await self.send_error(MESSAGE_NOT_VALID_CLIENT)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['message']
        message = Message(author=self.user, is_host=self.is_host, reservation_id=self.reservation_id,
                          text=text, created=timezone.now())
        data = MessageSerializer(message).data

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'data': data,
            }
        )

        await self.save(message)

    async def chat_message(self, event):
        data = {'type': 'chat_message'}
        data.update(event['data'])
        await self.send(text_data=json.dumps(data))
