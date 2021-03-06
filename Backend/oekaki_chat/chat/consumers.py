from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import urllib.parse
from .scripts.log_utils import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = urllib.parse.quote(self.scope['url_route']['kwargs']['room_name'])
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        # print_info('consumers', 'type(self.room_name), self.room_name :', type(self.room_name), self.room_name)
        # print_info('consumers', 'type(self.channel_name), self.channel_name : ', type(self.channel_name), self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text_data': text_data,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        text_data = event['text_data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text_data': text_data
        }))

