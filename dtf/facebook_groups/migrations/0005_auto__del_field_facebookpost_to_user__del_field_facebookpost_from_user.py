# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FacebookPost.to_user'
        db.delete_column(u'facebook_groups_facebookpost', 'to_user')

        # Deleting field 'FacebookPost.from_user'
        db.delete_column(u'facebook_groups_facebookpost', 'from_user')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'FacebookPost.to_user'
        raise RuntimeError("Cannot reverse this migration. 'FacebookPost.to_user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'FacebookPost.to_user'
        db.add_column(u'facebook_groups_facebookpost', 'to_user',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'FacebookPost.from_user'
        raise RuntimeError("Cannot reverse this migration. 'FacebookPost.from_user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'FacebookPost.from_user'
        db.add_column(u'facebook_groups_facebookpost', 'from_user',
                      self.gf('django.db.models.fields.TextField')(),
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
        u'facebook_groups.facebookgroup': {
            'Meta': {'object_name': 'FacebookGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'feed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'pinned_post': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['facebook_groups.FacebookPost']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'venue': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'facebook_groups.facebookpost': {
            'Meta': {'object_name': 'FacebookPost'},
            '_from': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'actions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_time': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fb_uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'privacy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'to': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'updated_time': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['facebook_groups']