# chat/utils.py

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_message_to_websocket(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{user_id}',
        {
            'type': 'chat_message',
            'message': message,
        }
    )
