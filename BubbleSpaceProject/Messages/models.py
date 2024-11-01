# models.py
from django.db import models
from django.conf import settings

class Chat(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_chats', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_chats', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat between {self.sender} and {self.recipient}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} on {self.date_sent}"
