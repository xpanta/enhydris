# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProcessBatch'
        db.create_table(u'hprocessor_processbatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('unique_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'hprocessor', ['ProcessBatch'])

        # Adding model 'ProcessUnit'
        db.create_table(u'hprocessor_processunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hprocessor.ProcessBatch'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('interpol_method', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('independent_column', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dependent_column', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('append_only', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('output_timeseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Timeseries'])),
            ('curve', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.GentityGenericData'], null=True, blank=True)),
            ('aggregation_missing_allowed', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('aggregation_missing_flag', self.gf('django.db.models.fields.CharField')(default='MISSING', max_length=16)),
            ('aggregation_last_incomplete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('aggregation_all_incomplete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hprocessor', ['ProcessUnit'])

        # Adding model 'ProcessInputVariable'
        db.create_table(u'hprocessor_processinputvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('process_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hprocessor.ProcessUnit'])),
            ('spec', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('timeseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Timeseries'])),
        ))
        db.send_create_signal(u'hprocessor', ['ProcessInputVariable'])


    def backwards(self, orm):
        # Deleting model 'ProcessBatch'
        db.delete_table(u'hprocessor_processbatch')

        # Deleting model 'ProcessUnit'
        db.delete_table(u'hprocessor_processunit')

        # Deleting model 'ProcessInputVariable'
        db.delete_table(u'hprocessor_processinputvariable')


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
        u'dbsync.database': {
            'Meta': {'object_name': 'Database'},
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'hcore.garea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Garea', '_ormbases': [u'hcore.Gentity']},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'gentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gentity']", 'unique': 'True', 'primary_key': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.gentity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Gentity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'political_division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.PoliticalDivision']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_alt': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'water_basin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.WaterBasin']", 'null': 'True', 'blank': 'True'}),
            'water_division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.WaterDivision']", 'null': 'True', 'blank': 'True'})
        },
        u'hcore.gentitygenericdata': {
            'Meta': {'object_name': 'GentityGenericData'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'data_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.GentityGenericDataType']"}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gentity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Gentity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'hcore.gentitygenericdatatype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'GentityGenericDataType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'file_extension': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.gpoint': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Gpoint', '_ormbases': [u'hcore.Gentity']},
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'approximate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asrid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'gentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gentity']", 'unique': 'True', 'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'srid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.instrument': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Instrument'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name_alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Station']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.InstrumentType']"})
        },
        u'hcore.instrumenttype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'InstrumentType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.intervaltype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'IntervalType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hcore.lentity': {
            'Meta': {'ordering': "('ordering_string',)", 'object_name': 'Lentity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'ordering_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'hcore.overseer': {
            'Meta': {'object_name': 'Overseer'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Person']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Station']"})
        },
        u'hcore.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person', '_ormbases': [u'hcore.Lentity']},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name_alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'initials_alt': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name_alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'lentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Lentity']", 'unique': 'True', 'primary_key': 'True'}),
            'middle_names': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'middle_names_alt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'hcore.politicaldivision': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PoliticalDivision', '_ormbases': [u'hcore.Garea']},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            u'garea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Garea']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.PoliticalDivision']", 'null': 'True', 'blank': 'True'})
        },
        u'hcore.station': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Station', '_ormbases': [u'hcore.Gpoint']},
            'copyright_holder': ('django.db.models.fields.TextField', [], {}),
            'copyright_years': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_stations'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'gpoint_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gpoint']", 'unique': 'True', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_automatic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'maintainers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'maintaining_stations'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'overseers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'stations_overseen'", 'symmetrical': 'False', 'through': u"orm['hcore.Overseer']", 'to': u"orm['hcore.Person']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_stations'", 'to': u"orm['hcore.Lentity']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stype': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hcore.StationType']", 'symmetrical': 'False'})
        },
        u'hcore.stationtype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'StationType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.timeseries': {
            'Meta': {'ordering': "('hidden',)", 'object_name': 'Timeseries'},
            'actual_offset_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'actual_offset_months': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gentity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeseries'", 'to': u"orm['hcore.Gentity']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Instrument']", 'null': 'True', 'blank': 'True'}),
            'interval_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.IntervalType']", 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_alt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'nominal_offset_minutes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nominal_offset_months': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'precision': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'time_step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.TimeStep']", 'null': 'True', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.TimeZone']"}),
            'unit_of_measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.UnitOfMeasurement']"}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Variable']"})
        },
        u'hcore.timestep': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'TimeStep'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'length_minutes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'length_months': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.timezone': {
            'Meta': {'ordering': "('utc_offset',)", 'object_name': 'TimeZone'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'utc_offset': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'hcore.unitofmeasurement': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'UnitOfMeasurement'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'variables': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hcore.Variable']", 'symmetrical': 'False'})
        },
        u'hcore.variable': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Variable'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.waterbasin': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBasin', '_ormbases': [u'hcore.Garea']},
            u'garea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Garea']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.WaterBasin']", 'null': 'True', 'blank': 'True'}),
            'water_division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.WaterDivision']", 'null': 'True', 'blank': 'True'})
        },
        u'hcore.waterdivision': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterDivision', '_ormbases': [u'hcore.Garea']},
            u'garea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Garea']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'hprocessor.processbatch': {
            'Meta': {'object_name': 'ProcessBatch'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'hprocessor.processinputvariable': {
            'Meta': {'object_name': 'ProcessInputVariable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hprocessor.ProcessUnit']"}),
            'spec': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Timeseries']"})
        },
        u'hprocessor.processunit': {
            'Meta': {'object_name': 'ProcessUnit'},
            'aggregation_all_incomplete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aggregation_last_incomplete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aggregation_missing_allowed': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'aggregation_missing_flag': ('django.db.models.fields.CharField', [], {'default': "'MISSING'", 'max_length': '16'}),
            'append_only': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hprocessor.ProcessBatch']"}),
            'curve': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.GentityGenericData']", 'null': 'True', 'blank': 'True'}),
            'dependent_column': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'independent_column': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'interpol_method': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'output_timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Timeseries']"})
        }
    }

    complete_apps = ['hprocessor']