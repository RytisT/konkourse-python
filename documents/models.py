from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from courses.models import Course
from filesize import size
import os


class DocumentManager(models.Manager):

    def getDocuments(self, user):
        documents = []
        relations = self.filter(owner=user).select_related(depth=1)
        for document in relations:
            documents.append(document)
        relations = self.filter(recipients=user)
        for document in relations:
            documents.append(document)
        return documents


def getPath(instance, filename):
    path = instance.owner.username + '/' + filename
    return path


class Document(models.Model):

    FILE_TYPES = (
        ('W', 'ms-word'),
        ('E', 'ms-excel'),
        ('O', 'ms-powerpoint'),
        ('P', 'pdf'),
        ('Z', 'zip'),
    )

    filename = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='owner')
    recipients = models.ManyToManyField(User)
    course = models.ManyToManyField(Course)
    file = models.FileField(upload_to=getPath)
    file_type = models.CharField(max_length=1, choices=FILE_TYPES)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    objects = DocumentManager()

    def getFileSize(self):
        return size(os.path.getsize(settings.MEDIA_ROOT + self.file.name))

    def getObjectType(self):
        return "Document"

    def __unicode__(self):
        return self.filename
