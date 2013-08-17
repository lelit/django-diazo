# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Theme.rules'
        db.add_column(u'django_diazo_theme', 'rules',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='themes', null=True, to=orm['django_diazo.Rule']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Theme.rules'
        db.delete_column(u'django_diazo_theme', 'rules_id')


    models = {
        u'django_diazo.compoundrule': {
            'Meta': {'object_name': 'CompoundRule', '_ormbases': [u'django_diazo.Rule']},
            'prefix': ('django.db.models.fields.TextField', [], {}),
            u'rule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_diazo.Rule']", 'unique': 'True', 'primary_key': 'True'}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'compound_rule'", 'symmetrical': 'False', 'to': u"orm['django_diazo.Rule']"}),
            'suffix': ('django.db.models.fields.TextField', [], {})
        },
        u'django_diazo.rule': {
            'Meta': {'object_name': 'Rule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_diazo.singlerule': {
            'Meta': {'object_name': 'SingleRule', '_ormbases': [u'django_diazo.Rule']},
            'rule': ('django.db.models.fields.TextField', [], {}),
            u'rule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_diazo.Rule']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'django_diazo.theme': {
            'Meta': {'object_name': 'Theme'},
            'builtin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'debug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rules': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'themes'", 'null': 'True', 'to': u"orm['django_diazo.Rule']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_diazo']