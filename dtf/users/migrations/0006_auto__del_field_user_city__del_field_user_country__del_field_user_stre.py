# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.city'
        db.delete_column(u'users_user', 'city')

        # Deleting field 'User.country'
        db.delete_column(u'users_user', 'country')

        # Deleting field 'User.street2'
        db.delete_column(u'users_user', 'street2')

        # Deleting field 'User.state'
        db.delete_column(u'users_user', 'state')

        # Deleting field 'User.street1'
        db.delete_column(u'users_user', 'street1')

        # Deleting field 'User.postal_code'
        db.delete_column(u'users_user', 'postal_code')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'User.city'
        raise RuntimeError("Cannot reverse this migration. 'User.city' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.city'
        db.add_column(u'users_user', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Adding field 'User.country'
        db.add_column(u'users_user', 'country',
                      self.gf('django.db.models.fields.CharField')(default='US', max_length=255),
                      keep_default=False)

        # Adding field 'User.street2'
        db.add_column(u'users_user', 'street2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'User.state'
        raise RuntimeError("Cannot reverse this migration. 'User.state' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.state'
        db.add_column(u'users_user', 'state',
                      self.gf('localflavor.us.models.USStateField')(max_length=2),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'User.street1'
        raise RuntimeError("Cannot reverse this migration. 'User.street1' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.street1'
        db.add_column(u'users_user', 'street1',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'User.postal_code'
        raise RuntimeError("Cannot reverse this migration. 'User.postal_code' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.postal_code'
        db.add_column(u'users_user', 'postal_code',
                      self.gf('django.db.models.fields.CharField')(max_length=10),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['users']