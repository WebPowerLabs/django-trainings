# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table(u'packages_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'packages', ['Package'])

        # Adding M2M table for field courses on 'Package'
        m2m_table_name = db.shorten_name(u'packages_package_courses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'packages.package'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', 'course_id'])

        # Adding M2M table for field lessons on 'Package'
        m2m_table_name = db.shorten_name(u'packages_package_lessons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'packages.package'], null=False)),
            ('lesson', models.ForeignKey(orm[u'lessons.lesson'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', 'lesson_id'])

        # Adding model 'PackagePurchase'
        db.create_table(u'packages_packagepurchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Package'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('data', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'packages', ['PackagePurchase'])

        # Adding model 'InfusionsoftPackage'
        db.create_table(u'packages_infusionsoftpackage', (
            (u'package_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['packages.Package'], unique=True, primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('product_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cycle', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('frequency', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pre_authorize_amount', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('prorate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('plan_price', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('action_set_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tag', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['packages.InfusionsoftTag'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'packages', ['InfusionsoftPackage'])

        # Adding model 'InfusionsoftTag'
        db.create_table(u'packages_infusionsofttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.TextField')()),
            ('group_category_id', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'packages', ['InfusionsoftTag'])


    def backwards(self, orm):
        # Deleting model 'Package'
        db.delete_table(u'packages_package')

        # Removing M2M table for field courses on 'Package'
        db.delete_table(db.shorten_name(u'packages_package_courses'))

        # Removing M2M table for field lessons on 'Package'
        db.delete_table(db.shorten_name(u'packages_package_lessons'))

        # Deleting model 'PackagePurchase'
        db.delete_table(u'packages_packagepurchase')

        # Deleting model 'InfusionsoftPackage'
        db.delete_table(u'packages_infusionsoftpackage')

        # Deleting model 'InfusionsoftTag'
        db.delete_table(u'packages_infusionsofttag')


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
        u'courses.content': {
            'Meta': {'object_name': 'Content'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_courses.content_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'thumbnail_height': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'courses.course': {
            'Meta': {'ordering': "['order']", 'object_name': 'Course', '_ormbases': [u'courses.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['courses.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'lessons.lesson': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Lesson', '_ormbases': [u'courses.Content']},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['courses.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            'homework': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tags.Tag']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'packages.infusionsoftpackage': {
            'Meta': {'object_name': 'InfusionsoftPackage', '_ormbases': [u'packages.Package']},
            'action_set_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'active': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cycle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'frequency': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'package_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['packages.Package']", 'unique': 'True', 'primary_key': 'True'}),
            'plan_price': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pre_authorize_amount': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'product_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'prorate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remote_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tag': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['packages.InfusionsoftTag']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'packages.infusionsofttag': {
            'Meta': {'object_name': 'InfusionsoftTag'},
            'group_category_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.TextField', [], {})
        },
        u'packages.package': {
            'Meta': {'object_name': 'Package'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lessons.Lesson']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'packages.packagepurchase': {
            'Meta': {'object_name': 'PackagePurchase'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['packages.Package']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'})
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

    complete_apps = ['packages']