from django.db import models
from django.contrib.auth import models as auth_models
# models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    time = models.DateTimeField()
    creator = models.ForeignKey(auth_models.User, related_name='event_creator_user')
    attendees = models.ManyToManyField(auth_models.User, related_name='event_attendees_user')


class File(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    creator = models.ForeignKey(auth_models.User, related_name='file_creator_user')
    modifier = models.ForeignKey(auth_models.User, related_name='file_modifier_user')
