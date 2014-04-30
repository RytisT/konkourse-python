# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings
from django.core.files import File
import os
#

class Migration(DataMigration):

    def forwards(self, orm):
	Page = orm['page.Page']
	virginia_tech = Page(title='Virginia Tech')
	virginia_tech.save()
	image = open(settings.DEFAULT_PATH + '/static/img/logos/vt-logo.jpg')
	virginia_tech.image.save(os.path.basename(image.name), File(image))

	jmu = Page(title='James Madison University')
	jmu.save()
	image = open(settings.DEFAULT_PATH + '/static/img/logos/jmu-logo.jpg')
	jmu.image.save(os.path.basename(image.name), File(image))

	uva = Page(title='University of Virginia')
	uva.save()
	image = open(settings.DEFAULT_PATH + '/static/img/logos/uva-logo.jpg')
	uva.image.save(os.path.basename(image.name), File(image))

	konkourse = Page(title='Konkourse')
	konkourse.save()
	image = open(settings.DEFAULT_PATH + '/static/img/logos/konkourse.png')
	konkourse.image.save(os.path.basename(image.name), File(image))



    models = {
        u'page.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': "'1000'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'30'"})
        }
    }

    complete_apps = ['page', 'data']
    symmetrical = True
