# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Technology.frequency_of_use_default'
        db.add_column('tl_technology', 'frequency_of_use_default', self.gf('django.db.models.fields.FloatField')(default=1, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Technology.frequency_of_use_default'
        db.delete_column('tl_technology', 'frequency_of_use_default')


    models = {
        'tl.brand': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Brand'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tl.Technology']"})
        },
        'tl.specification': {
            'Meta': {'unique_together': "(('id', 'no', 'i', 'j'),)", 'object_name': 'Specification'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tl.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tl.SpecificationCategory']"}),
            'i': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'no': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tl.Unit']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'tl.specificationcategory': {
            'Meta': {'object_name': 'SpecificationCategory'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tl.technology': {
            'Meta': {'object_name': 'Technology'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'frequency_of_use_default': ('django.db.models.fields.FloatField', [], {'default': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'tl.unit': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Unit'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['tl']
