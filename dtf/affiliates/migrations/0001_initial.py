# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zip'
        db.create_table(u'affiliates_zip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('affiliate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.Affiliate'])),
            ('postal_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal(u'affiliates', ['Zip'])

        # Adding model 'Affiliate'
        db.create_table(u'affiliates_affiliate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'affiliates', ['Affiliate'])


    def backwards(self, orm):
        # Deleting model 'Zip'
        db.delete_table(u'affiliates_zip')

        # Deleting model 'Affiliate'
        db.delete_table(u'affiliates_affiliate')


    models = {
        u'affiliates.affiliate': {
            'Meta': {'object_name': 'Affiliate'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'affiliates.zip': {
            'Meta': {'object_name': 'Zip'},
            'affiliate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['affiliates.Affiliate']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['affiliates']