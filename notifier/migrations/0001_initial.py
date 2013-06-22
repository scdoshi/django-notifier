# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Notifier'
        db.create_table(u'notifier_notifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'notifier', ['Notifier'])

        # Adding model 'Notification'
        db.create_table(u'notifier_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'notifier', ['Notification'])

        # Adding M2M table for field permissions on 'Notification'
        m2m_table_name = db.shorten_name(u'notifier_notification_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notification', models.ForeignKey(orm[u'notifier.notification'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notification_id', 'permission_id'])

        # Adding M2M table for field notifiers on 'Notification'
        m2m_table_name = db.shorten_name(u'notifier_notification_notifiers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notification', models.ForeignKey(orm[u'notifier.notification'], null=False)),
            ('notifier', models.ForeignKey(orm[u'notifier.notifier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notification_id', 'notifier_id'])

        # Adding model 'GroupNotify'
        db.create_table(u'notifier_groupnotify', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notification'])),
            ('notifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notifier'])),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'notifier', ['GroupNotify'])

        # Adding unique constraint on 'GroupNotify', fields ['group', 'notification', 'notifier']
        db.create_unique(u'notifier_groupnotify', ['group_id', 'notification_id', 'notifier_id'])

        # Adding model 'UserNotify'
        db.create_table(u'notifier_usernotify', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notification'])),
            ('notifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notifier'])),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'notifier', ['UserNotify'])

        # Adding unique constraint on 'UserNotify', fields ['user', 'notification', 'notifier']
        db.create_unique(u'notifier_usernotify', ['user_id', 'notification_id', 'notifier_id'])

        # Adding model 'SentNotification'
        db.create_table(u'notifier_sentnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 21, 0, 0), db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notification'])),
            ('notifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Notifier'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'notifier', ['SentNotification'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserNotify', fields ['user', 'notification', 'notifier']
        db.delete_unique(u'notifier_usernotify', ['user_id', 'notification_id', 'notifier_id'])

        # Removing unique constraint on 'GroupNotify', fields ['group', 'notification', 'notifier']
        db.delete_unique(u'notifier_groupnotify', ['group_id', 'notification_id', 'notifier_id'])

        # Deleting model 'Notifier'
        db.delete_table(u'notifier_notifier')

        # Deleting model 'Notification'
        db.delete_table(u'notifier_notification')

        # Removing M2M table for field permissions on 'Notification'
        db.delete_table(db.shorten_name(u'notifier_notification_permissions'))

        # Removing M2M table for field notifiers on 'Notification'
        db.delete_table(db.shorten_name(u'notifier_notification_notifiers'))

        # Deleting model 'GroupNotify'
        db.delete_table(u'notifier_groupnotify')

        # Deleting model 'UserNotify'
        db.delete_table(u'notifier_usernotify')

        # Deleting model 'SentNotification'
        db.delete_table(u'notifier_sentnotification')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notifier.groupnotify': {
            'Meta': {'unique_together': "(('group', 'notification', 'notifier'),)", 'object_name': 'GroupNotify'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notification']"}),
            'notifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notifier']"}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'})
        },
        u'notifier.notification': {
            'Meta': {'object_name': 'Notification'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'notifiers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['notifier.Notifier']", 'symmetrical': 'False', 'blank': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'})
        },
        u'notifier.notifier': {
            'Meta': {'object_name': 'Notifier'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'})
        },
        u'notifier.sentnotification': {
            'Meta': {'object_name': 'SentNotification'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notification']"}),
            'notifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notifier']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'notifier.usernotify': {
            'Meta': {'unique_together': "(('user', 'notification', 'notifier'),)", 'object_name': 'UserNotify'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notification']"}),
            'notifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Notifier']"}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 21, 0, 0)', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['notifier']