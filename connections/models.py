from django.db import models
from django.contrib.auth.models import User
from notifications import notify


class ConnectionManager(models.Manager):

    def connected(self, user1, user2):
        if (self.filter(creator=user1, acceptor=user2).count() == 1):
            return True
        elif (self.filter(creator=user2, acceptor=user1).count() == 1):
            return True
        else:
            return False

    def getConnections(self, user):
        connections = []
        relations = self.filter(creator=user).select_related(depth=1)
        for connection in relations:
            connections.append(connection.acceptor)
        relations = self.filter(acceptor=user).select_related(depth=1)
        for connection in relations:
            connections.append(connection.creator)

        return connections


class Connection(models.Model):
    created = models.DateTimeField('created', auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator')
    acceptor = models.ForeignKey(User, related_name='acceptor')
    objects = ConnectionManager()

    def getObjectType(self):
        return "Connection"


class RequestManager(models.Manager):

    def getRequests(self, user):
        requests = []
        relations = self.filter(reciever=user).select_related(depth=1)
        for request in relations:
            requests.append({"creator": request.creator, "request": request})

        return requests

    def requestSent(self, user1, user2):
        if (self.filter(creator=user1, reciever=user2).count() >= 1):
            return True
        else:
            return False

    def requestReceived(self, user1, user2):
        if (self.filter(creator=user2, reciever=user1).count() == 1):
            return True
        else:
            return False


class ConnectionRequest(models.Model):
    created = models.DateTimeField('created', auto_now_add=True)
    creator = models.ForeignKey(User, related_name='request_creator')
    reciever = models.ForeignKey(User, related_name='request_reciever')
    message = models.TextField(default="Would like to connect?")
    hidden = models.BooleanField(default=False)
    objects = RequestManager()

    def getObjectType(self):
        return "ConnectionRequest"

    def save(self, *args, **kwargs):
        super(ConnectionRequest, self).save(*args, **kwargs)
        if not self.hidden:
            notify.send(self.creator, recipient=self.reciever, action_object=self, verb='sent you a')

    def accept(self):
        if not Connection.objects.connected(user1=self.creator, user2=self.reciever):
            connection = Connection(creator=self.creator, acceptor=self.reciever)
            connection.save()
            notify.send(self.reciever, recipient=self.creator, action_object=connection, verb='accepted your')
            self.delete()

    def hide(self):
        self.hidden = True
        self.save()
