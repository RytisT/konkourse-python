# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings


class Migration(DataMigration):

    def forwards(self, orm):
        Site = orm['sites.Site']
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = settings.DOMAIN_NAME
        site.name = settings.SITE_NAME
        site.save()

    
    models = {
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['sites', 'data']
    symmetrical = True
