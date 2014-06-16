# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InfusionsoftPackage.name'
        db.add_column(u'packages_infusionsoftpackage', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_actionSetId'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_actionSetId',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InfusionsoftPackage.name'
        db.delete_column(u'packages_infusionsoftpackage', 'name')

        # Deleting field 'InfusionsoftPackage.infusionsoft_actionSetId'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_actionSetId')


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
            'infusionsoft_Prorate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infusionsoft_actionSetId': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['packages']