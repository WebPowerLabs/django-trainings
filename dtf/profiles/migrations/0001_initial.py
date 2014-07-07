# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacebookProfile'
        db.create_table(u'profiles_facebookprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.User'], unique=True)),
            ('fb_uid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'profiles', ['FacebookProfile'])

        # Adding model 'InfusionsoftProfile'
        db.create_table(u'profiles_infusionsoftprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.User'], unique=True)),
            ('remote_id', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'profiles', ['InfusionsoftProfile'])

        # Adding M2M table for field tags on 'InfusionsoftProfile'
        m2m_table_name = db.shorten_name(u'profiles_infusionsoftprofile_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('infusionsoftprofile', models.ForeignKey(orm[u'profiles.infusionsoftprofile'], null=False)),
            ('infusionsofttag', models.ForeignKey(orm[u'packages.infusionsofttag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['infusionsoftprofile_id', 'infusionsofttag_id'])

        # Adding model 'InstructorProfile'
        db.create_table(u'profiles_instructorprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.User'], unique=True)),
        ))
        db.send_create_signal(u'profiles', ['InstructorProfile'])


    def backwards(self, orm):
        # Deleting model 'FacebookProfile'
        db.delete_table(u'profiles_facebookprofile')

        # Deleting model 'InfusionsoftProfile'
        db.delete_table(u'profiles_infusionsoftprofile')

        # Removing M2M table for field tags on 'InfusionsoftProfile'
        db.delete_table(db.shorten_name(u'profiles_infusionsoftprofile_tags'))

        # Deleting model 'InstructorProfile'
        db.delete_table(u'profiles_instructorprofile')


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
        u'packages.infusionsofttag': {
            'Meta': {'object_name': 'InfusionsoftTag'},
            'group_category_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'profiles.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'fb_uid': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.User']", 'unique': 'True'})
        },
        u'profiles.infusionsoftprofile': {
            'Meta': {'object_name': 'InfusionsoftProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'infusionsoft_profiles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['packages.InfusionsoftTag']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.User']", 'unique': 'True'})
        },
        u'profiles.instructorprofile': {
            'Meta': {'object_name': 'InstructorProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.User']", 'unique': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infusionsoft_uid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['profiles']