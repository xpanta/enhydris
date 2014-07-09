# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Forecast'
        db.create_table(u'unexe_forecast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('yearfile', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('dailyfile', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('yeardate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dailydate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'unexe', ['Forecast'])

        # Adding model 'userDMAstats'
        db.create_table(u'unexe_userdmastats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statsdate', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('statsperiod', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sumhouseholds', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sumoccupants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sumunits', self.gf('django.db.models.fields.FloatField')()),
            ('maxunits', self.gf('django.db.models.fields.FloatField')()),
            ('avgunits', self.gf('django.db.models.fields.FloatField')()),
            ('minunits', self.gf('django.db.models.fields.FloatField')()),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.Household'])),
            ('options', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'unexe', ['userDMAstats'])

        # Adding model 'DMAstats'
        db.create_table(u'unexe_dmastats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statsdate', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('statsperiod', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sumhouseholds', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sumoccupants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sumunits', self.gf('django.db.models.fields.FloatField')()),
            ('maxoccupants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('avgoccupants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('minoccupants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('maxunits', self.gf('django.db.models.fields.FloatField')()),
            ('avgunits', self.gf('django.db.models.fields.FloatField')()),
            ('minunits', self.gf('django.db.models.fields.FloatField')()),
            ('dma', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.DMA'])),
        ))
        db.send_create_signal(u'unexe', ['DMAstats'])


    def backwards(self, orm):
        # Deleting model 'Forecast'
        db.delete_table(u'unexe_forecast')

        # Deleting model 'userDMAstats'
        db.delete_table(u'unexe_userdmastats')

        # Deleting model 'DMAstats'
        db.delete_table(u'unexe_dmastats')


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
        u'hcore.gpoint': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Gpoint', '_ormbases': [u'hcore.Gentity']},
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'approximate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asrid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'gentity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gentity']", 'unique': 'True', 'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'srid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hcore.politicaldivision': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PoliticalDivision', '_ormbases': [u'hcore.Garea']},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            u'garea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Garea']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hcore.PoliticalDivision']", 'null': 'True', 'blank': 'True'})
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
        u'iwidget.arithmeticvalueitem': {
            'Meta': {'unique_together': "(('subcategory', 'household'),)", 'object_name': 'ArithmeticValueItem'},
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arithmetic_values_items'", 'to': u"orm['iwidget.Household']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.HouseholdValueSubcategory']"})
        },
        u'iwidget.constructionperiod': {
            'Meta': {'ordering': "('id',)", 'object_name': 'ConstructionPeriod'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.dma': {
            'Meta': {'ordering': "('name',)", 'object_name': 'DMA', '_ormbases': [u'hcore.Garea']},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'garea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Garea']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'socio_demographics': ('django.db.models.fields.TextField', [], {})
        },
        u'iwidget.efficientappliance': {
            'Meta': {'ordering': "('id',)", 'object_name': 'EfficientAppliance'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.household': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Household', '_ormbases': [u'hcore.Gpoint']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'arithmetic_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.HouseholdValueSubcategory']", 'through': u"orm['iwidget.ArithmeticValueItem']", 'symmetrical': 'False'}),
            'construction_period': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.ConstructionPeriod']", 'null': 'True', 'blank': 'True'}),
            'dma': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'households'", 'to': u"orm['iwidget.DMA']"}),
            'efficient_appliances': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.EfficientAppliance']", 'symmetrical': 'False', 'blank': 'True'}),
            u'gpoint_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Gpoint']", 'unique': 'True', 'primary_key': 'True'}),
            'neighbours': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.Household']", 'through': u"orm['iwidget.Neighbour']", 'symmetrical': 'False'}),
            'num_of_occupants': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'outdoor_facilities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.OutdoorFacility']", 'symmetrical': 'False', 'blank': 'True'}),
            'ownership_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.OwnershipStatus']", 'null': 'True', 'blank': 'True'}),
            'property_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'property_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.PropertyType']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'households'", 'to': u"orm['auth.User']"}),
            'water_dms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.WaterDMS']", 'symmetrical': 'False', 'blank': 'True'}),
            'water_heaters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['iwidget.WaterHeater']", 'symmetrical': 'False', 'blank': 'True'}),
            'water_pricing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.WaterPricingScheme']", 'null': 'True', 'blank': 'True'})
        },
        u'iwidget.householdvaluecategory': {
            'Meta': {'ordering': "('id',)", 'object_name': 'HouseholdValueCategory'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.householdvaluesubcategory': {
            'Meta': {'ordering': "('id',)", 'object_name': 'HouseholdValueSubcategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': u"orm['iwidget.HouseholdValueCategory']"}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'form_component': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.neighbour': {
            'Meta': {'unique_together': "(('household1', 'household2'),)", 'object_name': 'Neighbour'},
            'household1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'household1'", 'to': u"orm['iwidget.Household']"}),
            'household2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'household2'", 'to': u"orm['iwidget.Household']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'iwidget.outdoorfacility': {
            'Meta': {'ordering': "('id',)", 'object_name': 'OutdoorFacility'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.ownershipstatus': {
            'Meta': {'ordering': "('id',)", 'object_name': 'OwnershipStatus'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.propertytype': {
            'Meta': {'ordering': "('id',)", 'object_name': 'PropertyType'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.waterdms': {
            'Meta': {'ordering': "('id',)", 'object_name': 'WaterDMS'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.waterheater': {
            'Meta': {'ordering': "('id',)", 'object_name': 'WaterHeater'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.waterpricingscheme': {
            'Meta': {'ordering': "('id',)", 'object_name': 'WaterPricingScheme'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descr_alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'original_db': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsync.Database']", 'null': 'True'}),
            'original_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'unexe.dmastats': {
            'Meta': {'object_name': 'DMAstats'},
            'avgoccupants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'avgunits': ('django.db.models.fields.FloatField', [], {}),
            'dma': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.DMA']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxoccupants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'maxunits': ('django.db.models.fields.FloatField', [], {}),
            'minoccupants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'minunits': ('django.db.models.fields.FloatField', [], {}),
            'statsdate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'statsperiod': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sumhouseholds': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sumoccupants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sumunits': ('django.db.models.fields.FloatField', [], {})
        },
        u'unexe.forecast': {
            'Meta': {'object_name': 'Forecast'},
            'dailydate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dailyfile': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'yeardate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'yearfile': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'unexe.userdmastats': {
            'Meta': {'object_name': 'userDMAstats'},
            'avgunits': ('django.db.models.fields.FloatField', [], {}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.Household']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxunits': ('django.db.models.fields.FloatField', [], {}),
            'minunits': ('django.db.models.fields.FloatField', [], {}),
            'options': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'statsdate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'statsperiod': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sumhouseholds': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sumoccupants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sumunits': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['unexe']