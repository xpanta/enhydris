# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lentity'
        db.create_table(u'hcore_lentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ordering_string', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Lentity'])

        # Adding model 'Person'
        db.create_table(u'hcore_person', (
            (u'lentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Lentity'], unique=True, primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('middle_names', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('last_name_alt', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('first_name_alt', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('middle_names_alt', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('initials_alt', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Person'])

        # Adding model 'Organization'
        db.create_table(u'hcore_organization', (
            (u'lentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Lentity'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('name_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('acronym_alt', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Organization'])

        # Adding model 'Gentity'
        db.create_table(u'hcore_gentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('water_basin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.WaterBasin'], null=True, blank=True)),
            ('water_division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.WaterDivision'], null=True, blank=True)),
            ('political_division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.PoliticalDivision'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('short_name_alt', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Gentity'])

        # Adding model 'Gpoint'
        db.create_table(u'hcore_gpoint', (
            (u'gentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Gentity'], unique=True, primary_key=True)),
            ('srid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('approximate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('altitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('asrid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Gpoint'])

        # Adding model 'Gline'
        db.create_table(u'hcore_gline', (
            (u'gentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Gentity'], unique=True, primary_key=True)),
            ('gpoint1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='glines1', null=True, to=orm['hcore.Gpoint'])),
            ('gpoint2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='glines2', null=True, to=orm['hcore.Gpoint'])),
            ('length', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('linestring', self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Gline'])

        # Adding model 'Garea'
        db.create_table(u'hcore_garea', (
            (u'gentity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Gentity'], unique=True, primary_key=True)),
            ('area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mpoly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Garea'])

        # Adding model 'PoliticalDivision'
        db.create_table(u'hcore_politicaldivision', (
            (u'garea_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Garea'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.PoliticalDivision'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['PoliticalDivision'])

        # Adding model 'WaterDivision'
        db.create_table(u'hcore_waterdivision', (
            (u'garea_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Garea'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'hcore', ['WaterDivision'])

        # Adding model 'WaterBasin'
        db.create_table(u'hcore_waterbasin', (
            (u'garea_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Garea'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.WaterBasin'], null=True, blank=True)),
            ('water_division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.WaterDivision'], null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['WaterBasin'])

        # Adding model 'GentityAltCodeType'
        db.create_table(u'hcore_gentityaltcodetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['GentityAltCodeType'])

        # Adding model 'GentityAltCode'
        db.create_table(u'hcore_gentityaltcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('gentity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alt_codes', to=orm['hcore.Gentity'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.GentityAltCodeType'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'hcore', ['GentityAltCode'])

        # Adding model 'GentityGenericDataType'
        db.create_table(u'hcore_gentitygenericdatatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('file_extension', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'hcore', ['GentityGenericDataType'])

        # Adding model 'GentityGenericData'
        db.create_table(u'hcore_gentitygenericdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('gentity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Gentity'])),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('data_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.GentityGenericDataType'])),
        ))
        db.send_create_signal(u'hcore', ['GentityGenericData'])

        # Adding model 'FileType'
        db.create_table(u'hcore_filetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'hcore', ['FileType'])

        # Adding model 'GentityFile'
        db.create_table(u'hcore_gentityfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('gentity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Gentity'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('file_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.FileType'])),
            ('content', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hcore', ['GentityFile'])

        # Adding model 'EventType'
        db.create_table(u'hcore_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['EventType'])

        # Adding model 'GentityEvent'
        db.create_table(u'hcore_gentityevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('gentity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Gentity'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.EventType'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('report', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('report_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hcore', ['GentityEvent'])

        # Adding model 'StationType'
        db.create_table(u'hcore_stationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['StationType'])

        # Adding model 'Station'
        db.create_table(u'hcore_station', (
            (u'gpoint_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Gpoint'], unique=True, primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owned_stations', to=orm['hcore.Lentity'])),
            ('is_automatic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('copyright_holder', self.gf('django.db.models.fields.TextField')()),
            ('copyright_years', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created_stations', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'hcore', ['Station'])

        # Adding M2M table for field stype on 'Station'
        m2m_table_name = db.shorten_name(u'hcore_station_stype')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('station', models.ForeignKey(orm[u'hcore.station'], null=False)),
            ('stationtype', models.ForeignKey(orm[u'hcore.stationtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['station_id', 'stationtype_id'])

        # Adding M2M table for field maintainers on 'Station'
        m2m_table_name = db.shorten_name(u'hcore_station_maintainers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('station', models.ForeignKey(orm[u'hcore.station'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['station_id', 'user_id'])

        # Adding model 'Overseer'
        db.create_table(u'hcore_overseer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Station'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Person'])),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Overseer'])

        # Adding model 'InstrumentType'
        db.create_table(u'hcore_instrumenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['InstrumentType'])

        # Adding model 'Instrument'
        db.create_table(u'hcore_instrument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Station'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.InstrumentType'])),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_alt', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Instrument'])

        # Adding model 'Variable'
        db.create_table(u'hcore_variable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Variable'])

        # Adding model 'UnitOfMeasurement'
        db.create_table(u'hcore_unitofmeasurement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hcore', ['UnitOfMeasurement'])

        # Adding M2M table for field variables on 'UnitOfMeasurement'
        m2m_table_name = db.shorten_name(u'hcore_unitofmeasurement_variables')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unitofmeasurement', models.ForeignKey(orm[u'hcore.unitofmeasurement'], null=False)),
            ('variable', models.ForeignKey(orm[u'hcore.variable'], null=False))
        ))
        db.create_unique(m2m_table_name, ['unitofmeasurement_id', 'variable_id'])

        # Adding model 'TimeZone'
        db.create_table(u'hcore_timezone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('utc_offset', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'hcore', ['TimeZone'])

        # Adding model 'TimeStep'
        db.create_table(u'hcore_timestep', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('length_minutes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('length_months', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'hcore', ['TimeStep'])

        # Adding model 'IntervalType'
        db.create_table(u'hcore_intervaltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hcore', ['IntervalType'])

        # Adding model 'Timeseries'
        db.create_table(u'hcore_timeseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('gentity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timeseries', to=orm['hcore.Gentity'])),
            ('variable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Variable'])),
            ('unit_of_measurement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.UnitOfMeasurement'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name_alt', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('precision', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('time_zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.TimeZone'])),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('remarks_alt', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Instrument'], null=True, blank=True)),
            ('time_step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.TimeStep'], null=True, blank=True)),
            ('interval_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.IntervalType'], null=True, blank=True)),
            ('nominal_offset_minutes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nominal_offset_months', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('actual_offset_minutes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('actual_offset_months', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hcore', ['Timeseries'])

        # Adding model 'TsRecords'
        db.create_table('ts_records', (
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hcore.Timeseries'], primary_key=True, db_column='id')),
            ('top', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('middle', self.gf('enhydris.hcore.models.BlobField')(null=True, blank=True)),
            ('bottom', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'hcore', ['TsRecords'])

        # Adding model 'UserProfile'
        db.create_table(u'hcore_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email_is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hcore', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Lentity'
        db.delete_table(u'hcore_lentity')

        # Deleting model 'Person'
        db.delete_table(u'hcore_person')

        # Deleting model 'Organization'
        db.delete_table(u'hcore_organization')

        # Deleting model 'Gentity'
        db.delete_table(u'hcore_gentity')

        # Deleting model 'Gpoint'
        db.delete_table(u'hcore_gpoint')

        # Deleting model 'Gline'
        db.delete_table(u'hcore_gline')

        # Deleting model 'Garea'
        db.delete_table(u'hcore_garea')

        # Deleting model 'PoliticalDivision'
        db.delete_table(u'hcore_politicaldivision')

        # Deleting model 'WaterDivision'
        db.delete_table(u'hcore_waterdivision')

        # Deleting model 'WaterBasin'
        db.delete_table(u'hcore_waterbasin')

        # Deleting model 'GentityAltCodeType'
        db.delete_table(u'hcore_gentityaltcodetype')

        # Deleting model 'GentityAltCode'
        db.delete_table(u'hcore_gentityaltcode')

        # Deleting model 'GentityGenericDataType'
        db.delete_table(u'hcore_gentitygenericdatatype')

        # Deleting model 'GentityGenericData'
        db.delete_table(u'hcore_gentitygenericdata')

        # Deleting model 'FileType'
        db.delete_table(u'hcore_filetype')

        # Deleting model 'GentityFile'
        db.delete_table(u'hcore_gentityfile')

        # Deleting model 'EventType'
        db.delete_table(u'hcore_eventtype')

        # Deleting model 'GentityEvent'
        db.delete_table(u'hcore_gentityevent')

        # Deleting model 'StationType'
        db.delete_table(u'hcore_stationtype')

        # Deleting model 'Station'
        db.delete_table(u'hcore_station')

        # Removing M2M table for field stype on 'Station'
        db.delete_table(db.shorten_name(u'hcore_station_stype'))

        # Removing M2M table for field maintainers on 'Station'
        db.delete_table(db.shorten_name(u'hcore_station_maintainers'))

        # Deleting model 'Overseer'
        db.delete_table(u'hcore_overseer')

        # Deleting model 'InstrumentType'
        db.delete_table(u'hcore_instrumenttype')

        # Deleting model 'Instrument'
        db.delete_table(u'hcore_instrument')

        # Deleting model 'Variable'
        db.delete_table(u'hcore_variable')

        # Deleting model 'UnitOfMeasurement'
        db.delete_table(u'hcore_unitofmeasurement')

        # Removing M2M table for field variables on 'UnitOfMeasurement'
        db.delete_table(db.shorten_name(u'hcore_unitofmeasurement_variables'))

        # Deleting model 'TimeZone'
        db.delete_table(u'hcore_timezone')

        # Deleting model 'TimeStep'
        db.delete_table(u'hcore_timestep')

        # Deleting model 'IntervalType'
        db.delete_table(u'hcore_intervaltype')

        # Deleting model 'Timeseries'
        db.delete_table(u'hcore_timeseries')

        # Deleting model 'TsRecords'
        db.delete_table('ts_records')

        # Deleting model 'UserProfile'
        db.delete_table(u'hcore_userprofile')


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
        u'hcore.eventtype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'EventType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.filetype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'FileType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        u'hcore.gentityaltcode': {
            'Meta': {'object_name': 'GentityAltCode'},
            'gentity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alt_codes'", 'to': u"orm['hcore.Gentity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.GentityAltCodeType']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hcore.gentityaltcodetype': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'GentityAltCodeType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.gentityevent': {
            'Meta': {'ordering': "['-date']", 'object_name': 'GentityEvent'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'gentity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Gentity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.EventType']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'hcore.gentityfile': {
            'Meta': {'object_name': 'GentityFile'},
            'content': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.FileType']"}),
            'gentity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Gentity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remarks_alt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
        u'hcore.gline': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Gline', '_ormbases': [u'hcore.Gentity']},
            u'gentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gentity']", 'unique': 'True', 'primary_key': 'True'}),
            'gpoint1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glines1'", 'null': 'True', 'to': u"orm['hcore.Gpoint']"}),
            'gpoint2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glines2'", 'null': 'True', 'to': u"orm['hcore.Gpoint']"}),
            'length': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'linestring': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True', 'blank': 'True'})
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
        u'hcore.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization', '_ormbases': [u'hcore.Lentity']},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'acronym_alt': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'lentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Lentity']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
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
        u'hcore.tsrecords': {
            'Meta': {'object_name': 'TsRecords', 'db_table': "'ts_records'"},
            'bottom': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.Timeseries']", 'primary_key': 'True', 'db_column': "'id'"}),
            'middle': ('enhydris.hcore.models.BlobField', [], {'null': 'True', 'blank': 'True'}),
            'top': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
        u'hcore.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
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
        }
    }

    complete_apps = ['hcore']