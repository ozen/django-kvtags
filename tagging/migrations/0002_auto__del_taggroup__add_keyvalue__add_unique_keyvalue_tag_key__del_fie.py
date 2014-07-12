# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'TaggedItem', fields ['tag_group', 'object_id', 'content_type']
        db.delete_unique(u'tagging_taggeditem', ['tag_group_id', 'object_id', 'content_type_id'])

        # Removing unique constraint on 'Tag', fields ['tag_group', 'key']
        db.delete_unique(u'tagging_tag', ['tag_group_id', 'key'])

        # Deleting model 'TagGroup'
        db.delete_table(u'tagging_taggroup')

        # Adding model 'KeyValue'
        db.create_table(u'tagging_keyvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keyvalues', to=orm['tagging.Tag'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tagging', ['KeyValue'])

        # Adding unique constraint on 'KeyValue', fields ['tag', 'key']
        db.create_unique(u'tagging_keyvalue', ['tag_id', 'key'])

        # Deleting field 'Tag.tag_group'
        db.delete_column(u'tagging_tag', 'tag_group_id')

        # Deleting field 'Tag.value'
        db.delete_column(u'tagging_tag', 'value')

        # Deleting field 'TaggedItem.tag_group'
        db.delete_column(u'tagging_taggeditem', 'tag_group_id')

        # Adding field 'TaggedItem.tag'
        db.add_column(u'tagging_taggeditem', 'tag',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', null=True, to=orm['tagging.Tag']),
                      keep_default=False)

        # Adding unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.create_unique(u'tagging_taggeditem', ['tag_id', 'object_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TaggedItem', fields ['tag', 'object_id', 'content_type']
        db.delete_unique(u'tagging_taggeditem', ['tag_id', 'object_id', 'content_type_id'])

        # Removing unique constraint on 'KeyValue', fields ['tag', 'key']
        db.delete_unique(u'tagging_keyvalue', ['tag_id', 'key'])

        # Adding model 'TagGroup'
        db.create_table(u'tagging_taggroup', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'tagging', ['TagGroup'])

        # Deleting model 'KeyValue'
        db.delete_table(u'tagging_keyvalue')


        # User chose to not deal with backwards NULL issues for 'Tag.tag_group'
        raise RuntimeError("Cannot reverse this migration. 'Tag.tag_group' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tag.tag_group'
        db.add_column(u'tagging_tag', 'tag_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.TagGroup']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Tag.value'
        raise RuntimeError("Cannot reverse this migration. 'Tag.value' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tag.value'
        db.add_column(u'tagging_tag', 'value',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)

        # Adding unique constraint on 'Tag', fields ['tag_group', 'key']
        db.create_unique(u'tagging_tag', ['tag_group_id', 'key'])


        # User chose to not deal with backwards NULL issues for 'TaggedItem.tag_group'
        raise RuntimeError("Cannot reverse this migration. 'TaggedItem.tag_group' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TaggedItem.tag_group'
        db.add_column(u'tagging_taggeditem', 'tag_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.TagGroup']),
                      keep_default=False)

        # Deleting field 'TaggedItem.tag'
        db.delete_column(u'tagging_taggeditem', 'tag_id')

        # Adding unique constraint on 'TaggedItem', fields ['tag_group', 'object_id', 'content_type']
        db.create_unique(u'tagging_taggeditem', ['tag_group_id', 'object_id', 'content_type_id'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tagging.keyvalue': {
            'Meta': {'unique_together': "(('tag', 'key'),)", 'object_name': 'KeyValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keyvalues'", 'to': u"orm['tagging.Tag']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tagging.tag': {
            'Meta': {'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'object_id', 'content_type'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'null': 'True', 'to': u"orm['tagging.Tag']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['tagging']