from django.db import models
from django.conf import settings
from django.core.files import File
# Create your models here.


def getPath(instance, filename):
    path = 'page_' + str(instance.id) + '/' + filename
    return path


class Page(models.Model):
    title = models.CharField(max_length='30')
    image = models.ImageField(upload_to=getPath)
    description = models.CharField(max_length='1000')
