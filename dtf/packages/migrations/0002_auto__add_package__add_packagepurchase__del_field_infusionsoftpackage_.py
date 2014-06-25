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

        # Adding M2M table for field course on 'Package'
        m2m_table_name = db.shorten_name(u'packages_package_course')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'packages.package'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', 'course_id'])

        # Adding model 'PackagePurchase'
        db.create_table(u'packages_packagepurchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Package'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'packages', ['PackagePurchase'])

        # Deleting field 'InfusionsoftPackage.infusionsoft_Frequency'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_Frequency')

        # Deleting field 'InfusionsoftPackage.infusionsoft_Active'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_Active')

        # Deleting field 'InfusionsoftPackage.infusionsoft_Prorate'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_Prorate')

        # Deleting field 'InfusionsoftPackage.infusionsoft_ProductId'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_ProductId')

        # Deleting field 'InfusionsoftPackage.infusionsoft_PlanPrice'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_PlanPrice')

        # Deleting field 'InfusionsoftPackage.infusionsoft_PreAuthorizeAmount'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_PreAuthorizeAmount')

        # Deleting field 'InfusionsoftPackage.infusionsoft_Id'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_Id')

        # Deleting field 'InfusionsoftPackage.infusionsoft_Cycle'
        db.delete_column(u'packages_infusionsoftpackage', 'infusionsoft_Cycle')

        # Deleting field 'InfusionsoftPackage.id'
        db.delete_column(u'packages_infusionsoftpackage', u'id')

        # Adding field 'InfusionsoftPackage.package_ptr'
        db.add_column(u'packages_infusionsoftpackage', u'package_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['packages.Package'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.remote_id'
        db.add_column(u'packages_infusionsoftpackage', 'remote_id',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.product_id'
        db.add_column(u'packages_infusionsoftpackage', 'product_id',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.cycle'
        db.add_column(u'packages_infusionsoftpackage', 'cycle',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.frequency'
        db.add_column(u'packages_infusionsoftpackage', 'frequency',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.pre_authorize_amount'
        db.add_column(u'packages_infusionsoftpackage', 'pre_authorize_amount',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.prorate'
        db.add_column(u'packages_infusionsoftpackage', 'prorate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.active'
        db.add_column(u'packages_infusionsoftpackage', 'active',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.plan_price'
        db.add_column(u'packages_infusionsoftpackage', 'plan_price',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.action_set_id'
        db.add_column(u'packages_infusionsoftpackage', 'action_set_id',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Package'
        db.delete_table(u'packages_package')

        # Removing M2M table for field course on 'Package'
        db.delete_table(db.shorten_name(u'packages_package_course'))

        # Deleting model 'PackagePurchase'
        db.delete_table(u'packages_packagepurchase')

        # Adding field 'InfusionsoftPackage.infusionsoft_Frequency'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_Frequency',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_Active'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_Active',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_Prorate'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_Prorate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_ProductId'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_ProductId',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_PlanPrice'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_PlanPrice',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_PreAuthorizeAmount'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_PreAuthorizeAmount',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_Id'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_Id',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.infusionsoft_Cycle'
        db.add_column(u'packages_infusionsoftpackage', 'infusionsoft_Cycle',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InfusionsoftPackage.id'
        db.add_column(u'packages_infusionsoftpackage', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Deleting field 'InfusionsoftPackage.package_ptr'
        db.delete_column(u'packages_infusionsoftpackage', u'package_ptr_id')

        # Deleting field 'InfusionsoftPackage.remote_id'
        db.delete_column(u'packages_infusionsoftpackage', 'remote_id')

        # Deleting field 'InfusionsoftPackage.product_id'
        db.delete_column(u'packages_infusionsoftpackage', 'product_id')

        # Deleting field 'InfusionsoftPackage.cycle'
        db.delete_column(u'packages_infusionsoftpackage', 'cycle')

        # Deleting field 'InfusionsoftPackage.frequency'
        db.delete_column(u'packages_infusionsoftpackage', 'frequency')

        # Deleting field 'InfusionsoftPackage.pre_authorize_amount'
        db.delete_column(u'packages_infusionsoftpackage', 'pre_authorize_amount')

        # Deleting field 'InfusionsoftPackage.prorate'
        db.delete_column(u'packages_infusionsoftpackage', 'prorate')

        # Deleting field 'InfusionsoftPackage.active'
        db.delete_column(u'packages_infusionsoftpackage', 'active')

        # Deleting field 'InfusionsoftPackage.plan_price'
        db.delete_column(u'packages_infusionsoftpackage', 'plan_price')

        # Deleting field 'InfusionsoftPackage.action_set_id'
        db.delete_column(u'packages_infusionsoftpackage', 'action_set_id')


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
        u'courses.course': {
            'Meta': {'ordering': "['order']", 'object_name': 'Course'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'thumbnail_height': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'remote_id': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'packages.package': {
            'Meta': {'object_name': 'Package'},
            'course': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'packages.packagepurchase': {
            'Meta': {'object_name': 'PackagePurchase'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['packages.Package']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
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