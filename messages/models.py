from django.db import models
from account.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='message_sender')
    recipient = models.ManyToManyField(User, related_name='message_recipients')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="")
    header = models.CharField(max_length=180, default="")
    deleted = models.BooleanField(default=False)

class MessageChain(models.Model):
    messages = models.ManyToManyField(Message)
    new_message = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

class Inbox(models.Model):
    chains = models.ManyToManyField(MessageChain)
    owner = models.ForeignKey(User)





