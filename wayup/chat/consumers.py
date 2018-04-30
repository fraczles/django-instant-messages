from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Join a group named by current user's pk
        self.user = self.scope['user']

        async_to_sync(self.channel_layer.group_add)(
            str(self.user.pk),
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            str(self.user.pk),
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        """ Broadcasts the message to the author and recipient only """

        data = json.loads(text_data)

        Message.objects.create(
            author_id=self.user.pk,
            recipient_id=data['recipient'],
            body=data['message']
        )

        async_to_sync(self.channel_layer.group_add)(
            str(data['recipient']),
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            str(data['recipient']),
            {
                'type': 'chat_message',
                'message': data['message'],
                'user': data['user'],
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            str(data['recipient']),
            self.channel_name
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': '{}: {}'.format(user, message)
        }))
