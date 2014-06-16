# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InfusionsoftPackage'
        db.create_table(u'packages_infusionsoftpackage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('infusionsoft_Id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_ProductId', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_Cycle', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_Frequency', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_PreAuthorizeAmount', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_Prorate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_Active', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('infusionsoft_PlanPrice', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'packages', ['InfusionsoftPackage'])


    def backwards(self, orm):
        # Deleting model 'InfusionsoftPackage'
        db.delete_table(u'packages_infusionsoftpackage')


    models = {
        u'packages.infusionsoftpackage': {
            'Meta': {'object_name': 'InfusionsoftPackage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infusionsoft_Active': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_Cycle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_Frequency': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_Id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_PlanPrice': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_PreAuthorizeAmount': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_ProductId': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_Prorate': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['packages']