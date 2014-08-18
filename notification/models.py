from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class NotificationManager(models.Manager):

    def getAllNotifications(self, user):
        notes = []
        relations = self.filter(recipient=user).select_related(depth=1)
        for notification in relations:
            notes.append({"type": notification.type, "notification": notification})

        return notes

    def getNotificationByType(self, user, type):
        notes = []
        relations = self.filter(recipient=user, type=type).select_related(depth=1)
        for notification in relations:
            notes.append({"type": notification.type, "notification": notification})

        return notes


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('C', 'Course'),
        ('S', 'Social'),
        ('R', 'Requests'),
        ('O', 'Other'),
    )
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    message = models.TextField(default='This is an update')
    recipient = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = NotificationManager()

    def viewed(self):
        self.active = False
        self.save()
