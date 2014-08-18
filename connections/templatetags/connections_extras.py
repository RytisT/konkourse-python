from django import template
from connections.models import Connection, ConnectionRequest
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='connected')
def connected(instance, target_id):
    u = User.objects.get(id=target_id)
    connected = Connection.objects.connected(instance, u)
    return connected


@register.filter(name='requested')
def requested(instance, target_id):
    u = User.objects.get(id=target_id)
    requested = ConnectionRequest.objects.requestSent(instance, u)
    return requested


@register.filter(name='recieved')
def recieved(instance, target_id):
    u = User.objects.get(id=target_id)
    requested = ConnectionRequest.objects.requestReceived(instance, u)
    return requested
