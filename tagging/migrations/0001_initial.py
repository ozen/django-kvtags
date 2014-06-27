# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagGroup'
        db.create_table(u'tagging_taggroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('key', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'tagging', ['TagGroup'])

        # Adding model 'Tag'
        db.create_table(u'tagging_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('tag_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.TagGroup'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tagging', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['tag_group', 'key']
        db.create_unique(u'tagging_tag', ['tag_group_id', 'key'])

        # Adding model 'TaggedItem'
        db.create_table(u'tagging_taggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('tag_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.TagGroup'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'tagging', ['TaggedItem'])

        # Adding unique constraint on 'TaggedItem', fields ['tag_group', 'object_id', 'content_type']
        db.create_unique(u'tagging_taggeditem', ['tag_group_id', 'object_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TaggedItem', fields ['tag_group', 'object_id', 'content_type']
        db.delete_unique(u'tagging_taggeditem', ['tag_group_id', 'object_id', 'content_type_id'])

        # Removing unique constraint on 'Tag', fields ['tag_group', 'key']
        db.delete_unique(u'tagging_tag', ['tag_group_id', 'key'])

        # Deleting model 'TagGroup'
        db.delete_table(u'tagging_taggroup')

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
            'Meta': {'unique_together': "(('tag_group', 'key'),)", 'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'tag_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tagging.TagGroup']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag_group', 'object_id', 'content_type'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tagging.TagGroup']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'tagging.taggroup': {
            'Meta': {'object_name': 'TagGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['tagging']