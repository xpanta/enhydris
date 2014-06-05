# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Technology'
        db.create_table(u'tl_technology', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('frequency_of_use_default', self.gf('django.db.models.fields.FloatField')(default=1, blank=True)),
        ))
        db.send_create_signal(u'tl', ['Technology'])

        # Adding model 'Brand'
        db.create_table(u'tl_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('technology', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tl.Technology'])),
            ('old_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tl', ['Brand'])

        # Adding model 'Unit'
        db.create_table(u'tl_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'tl', ['Unit'])

        # Adding model 'SpecificationCategory'
        db.create_table(u'tl_specificationcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'tl', ['SpecificationCategory'])

        # Adding model 'Specification'
        db.create_table(u'tl_specification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tl.SpecificationCategory'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tl.Brand'])),
            ('no', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('i', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('j', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tl.Unit'], null=True, blank=True)),
        ))
        db.send_create_signal(u'tl', ['Specification'])

        # Adding unique constraint on 'Specification', fields [u'id', 'no', 'i', 'j']
        db.create_unique(u'tl_specification', [u'id', 'no', 'i', 'j'])


    def backwards(self, orm):
        # Removing unique constraint on 'Specification', fields [u'id', 'no', 'i', 'j']
        db.delete_unique(u'tl_specification', [u'id', 'no', 'i', 'j'])

        # Deleting model 'Technology'
        db.delete_table(u'tl_technology')

        # Deleting model 'Brand'
        db.delete_table(u'tl_brand')

        # Deleting model 'Unit'
        db.delete_table(u'tl_unit')

        # Deleting model 'SpecificationCategory'
        db.delete_table(u'tl_specificationcategory')

        # Deleting model 'Specification'
        db.delete_table(u'tl_specification')


    models = {
        u'tl.brand': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Brand'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tl.Technology']"})
        },
        u'tl.specification': {
            'Meta': {'unique_together': "(('id', 'no', 'i', 'j'),)", 'object_name': 'Specification'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tl.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tl.SpecificationCategory']"}),
            'i': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'j': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'no': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tl.Unit']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'tl.specificationcategory': {
            'Meta': {'object_name': 'SpecificationCategory'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'tl.technology': {
            'Meta': {'object_name': 'Technology'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'frequency_of_use_default': ('django.db.models.fields.FloatField', [], {'default': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'tl.unit': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Unit'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['tl']