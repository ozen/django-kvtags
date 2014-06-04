# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tagging_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_id', self.gf('django.db.models.fields.IntegerField')()),
            ('lang', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'tagging', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['tag_id', 'lang']
        db.create_unique(u'tagging_tag', ['tag_id', 'lang'])

        # Adding model 'TaggedItem'
        db.create_table(u'tagging_taggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_id', self.gf('django.db.models.fields.IntegerField')()),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal(u'tagging', ['TaggedItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['tag_id', 'lang']
        db.delete_unique(u'tagging_tag', ['tag_id', 'lang'])

        # Deleting model 'Tag'
        db.delete_table(u'tagging_tag')

        # Deleting model 'TaggedItem'
        db.delete_table(u'tagging_taggeditem')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tagging.tag': {
            'Meta': {'unique_together': "(('tag_id', 'lang'),)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tag_id': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'tagging.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'tag_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['tagging']