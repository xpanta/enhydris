# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DMA'
        db.create_table(u'iwidget_dma', (
            (u'garea_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Garea'], unique=True, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('socio_demographics', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'iwidget', ['DMA'])

        # Adding model 'PropertyType'
        db.create_table(u'iwidget_propertytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['PropertyType'])

        # Adding model 'ConstructionPeriod'
        db.create_table(u'iwidget_constructionperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['ConstructionPeriod'])

        # Adding model 'OwnershipStatus'
        db.create_table(u'iwidget_ownershipstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['OwnershipStatus'])

        # Adding model 'OutdoorFacility'
        db.create_table(u'iwidget_outdoorfacility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['OutdoorFacility'])

        # Adding model 'WaterHeater'
        db.create_table(u'iwidget_waterheater', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['WaterHeater'])

        # Adding model 'WaterPricingScheme'
        db.create_table(u'iwidget_waterpricingscheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['WaterPricingScheme'])

        # Adding model 'EfficientAppliance'
        db.create_table(u'iwidget_efficientappliance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['EfficientAppliance'])

        # Adding model 'WaterDMS'
        db.create_table(u'iwidget_waterdms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['WaterDMS'])

        # Adding model 'HouseholdValueCategory'
        db.create_table(u'iwidget_householdvaluecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['HouseholdValueCategory'])

        # Adding model 'HouseholdValueSubcategory'
        db.create_table(u'iwidget_householdvaluesubcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('original_db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsync.Database'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descr_alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subcategories', to=orm['iwidget.HouseholdValueCategory'])),
            ('form_component', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['HouseholdValueSubcategory'])

        # Adding model 'ArithmeticValueItem'
        db.create_table(u'iwidget_arithmeticvalueitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.HouseholdValueSubcategory'])),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(related_name='arithmetic_values_items', to=orm['iwidget.Household'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'iwidget', ['ArithmeticValueItem'])

        # Adding unique constraint on 'ArithmeticValueItem', fields ['subcategory', 'household']
        db.create_unique(u'iwidget_arithmeticvalueitem', ['subcategory_id', 'household_id'])

        # Adding model 'Household'
        db.create_table(u'iwidget_household', (
            (u'gpoint_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Gpoint'], unique=True, primary_key=True)),
            ('num_of_occupants', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='households', to=orm['auth.User'])),
            ('property_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.PropertyType'], null=True, blank=True)),
            ('property_size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dma', self.gf('django.db.models.fields.related.ForeignKey')(related_name='households', to=orm['iwidget.DMA'])),
            ('construction_period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.ConstructionPeriod'], null=True, blank=True)),
            ('ownership_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.OwnershipStatus'], null=True, blank=True)),
            ('water_pricing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.WaterPricingScheme'], null=True, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['Household'])

        # Adding M2M table for field outdoor_facilities on 'Household'
        m2m_table_name = db.shorten_name(u'iwidget_household_outdoor_facilities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('household', models.ForeignKey(orm[u'iwidget.household'], null=False)),
            ('outdoorfacility', models.ForeignKey(orm[u'iwidget.outdoorfacility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['household_id', 'outdoorfacility_id'])

        # Adding M2M table for field water_heaters on 'Household'
        m2m_table_name = db.shorten_name(u'iwidget_household_water_heaters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('household', models.ForeignKey(orm[u'iwidget.household'], null=False)),
            ('waterheater', models.ForeignKey(orm[u'iwidget.waterheater'], null=False))
        ))
        db.create_unique(m2m_table_name, ['household_id', 'waterheater_id'])

        # Adding M2M table for field efficient_appliances on 'Household'
        m2m_table_name = db.shorten_name(u'iwidget_household_efficient_appliances')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('household', models.ForeignKey(orm[u'iwidget.household'], null=False)),
            ('efficientappliance', models.ForeignKey(orm[u'iwidget.efficientappliance'], null=False))
        ))
        db.create_unique(m2m_table_name, ['household_id', 'efficientappliance_id'])

        # Adding M2M table for field water_dms on 'Household'
        m2m_table_name = db.shorten_name(u'iwidget_household_water_dms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('household', models.ForeignKey(orm[u'iwidget.household'], null=False)),
            ('waterdms', models.ForeignKey(orm[u'iwidget.waterdms'], null=False))
        ))
        db.create_unique(m2m_table_name, ['household_id', 'waterdms_id'])

        # Adding model 'Neighbour'
        db.create_table(u'iwidget_neighbour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('household1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='household1', to=orm['iwidget.Household'])),
            ('household2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='household2', to=orm['iwidget.Household'])),
        ))
        db.send_create_signal(u'iwidget', ['Neighbour'])

        # Adding unique constraint on 'Neighbour', fields ['household1', 'household2']
        db.create_unique(u'iwidget_neighbour', ['household1_id', 'household2_id'])

        # Adding model 'IWTimeseries'
        db.create_table(u'iwidget_iwtimeseries', (
            (u'timeseries_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Timeseries'], unique=True, primary_key=True)),
            ('typical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regular', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'iwidget', ['IWTimeseries'])

        # Adding model 'ApplianceTimeseries'
        db.create_table(u'iwidget_appliancetimeseries', (
            (u'timeseries_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Timeseries'], unique=True, primary_key=True)),
            ('appliance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timeseries', to=orm['iwidget.Appliance'])),
        ))
        db.send_create_signal(u'iwidget', ['ApplianceTimeseries'])

        # Adding model 'SmartMeter'
        db.create_table(u'iwidget_smartmeter', (
            (u'instrument_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hcore.Instrument'], unique=True, primary_key=True)),
            ('precision', self.gf('django.db.models.fields.IntegerField')(default=5, blank=True)),
            ('specs', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['SmartMeter'])

        # Adding model 'Appliance'
        db.create_table(u'iwidget_appliance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appliances', to=orm['tl.Brand'])),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appliances', to=orm['iwidget.Household'])),
        ))
        db.send_create_signal(u'iwidget', ['Appliance'])

        # Adding model 'ApplianceOperation'
        db.create_table(u'iwidget_applianceoperation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appliance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='operations', to=orm['iwidget.Appliance'])),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('scheduled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'iwidget', ['ApplianceOperation'])

        # Adding model 'Country'
        db.create_table(u'iwidget_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['Country'])

        # Adding model 'UserProfile'
        db.create_table(u'iwidget_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iwidget.Country'], null=True, blank=True)),
        ))
        db.send_create_signal(u'iwidget', ['UserProfile'])

        # Adding model 'UserValidationKey'
        db.create_table(u'iwidget_uservalidationkey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='validation_key', to=orm['auth.User'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sso', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('popup', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'iwidget', ['UserValidationKey'])

        # Adding model 'UserNotifications'
        db.create_table(u'iwidget_usernotifications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['auth.User'])),
            ('notification', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('detected', self.gf('django.db.models.fields.DateField')()),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remark', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
        ))
        db.send_create_signal(u'iwidget', ['UserNotifications'])


    def backwards(self, orm):
        # Removing unique constraint on 'Neighbour', fields ['household1', 'household2']
        db.delete_unique(u'iwidget_neighbour', ['household1_id', 'household2_id'])

        # Removing unique constraint on 'ArithmeticValueItem', fields ['subcategory', 'household']
        db.delete_unique(u'iwidget_arithmeticvalueitem', ['subcategory_id', 'household_id'])

        # Deleting model 'DMA'
        db.delete_table(u'iwidget_dma')

        # Deleting model 'PropertyType'
        db.delete_table(u'iwidget_propertytype')

        # Deleting model 'ConstructionPeriod'
        db.delete_table(u'iwidget_constructionperiod')

        # Deleting model 'OwnershipStatus'
        db.delete_table(u'iwidget_ownershipstatus')

        # Deleting model 'OutdoorFacility'
        db.delete_table(u'iwidget_outdoorfacility')

        # Deleting model 'WaterHeater'
        db.delete_table(u'iwidget_waterheater')

        # Deleting model 'WaterPricingScheme'
        db.delete_table(u'iwidget_waterpricingscheme')

        # Deleting model 'EfficientAppliance'
        db.delete_table(u'iwidget_efficientappliance')

        # Deleting model 'WaterDMS'
        db.delete_table(u'iwidget_waterdms')

        # Deleting model 'HouseholdValueCategory'
        db.delete_table(u'iwidget_householdvaluecategory')

        # Deleting model 'HouseholdValueSubcategory'
        db.delete_table(u'iwidget_householdvaluesubcategory')

        # Deleting model 'ArithmeticValueItem'
        db.delete_table(u'iwidget_arithmeticvalueitem')

        # Deleting model 'Household'
        db.delete_table(u'iwidget_household')

        # Removing M2M table for field outdoor_facilities on 'Household'
        db.delete_table(db.shorten_name(u'iwidget_household_outdoor_facilities'))

        # Removing M2M table for field water_heaters on 'Household'
        db.delete_table(db.shorten_name(u'iwidget_household_water_heaters'))

        # Removing M2M table for field efficient_appliances on 'Household'
        db.delete_table(db.shorten_name(u'iwidget_household_efficient_appliances'))

        # Removing M2M table for field water_dms on 'Household'
        db.delete_table(db.shorten_name(u'iwidget_household_water_dms'))

        # Deleting model 'Neighbour'
        db.delete_table(u'iwidget_neighbour')

        # Deleting model 'IWTimeseries'
        db.delete_table(u'iwidget_iwtimeseries')

        # Deleting model 'ApplianceTimeseries'
        db.delete_table(u'iwidget_appliancetimeseries')

        # Deleting model 'SmartMeter'
        db.delete_table(u'iwidget_smartmeter')

        # Deleting model 'Appliance'
        db.delete_table(u'iwidget_appliance')

        # Deleting model 'ApplianceOperation'
        db.delete_table(u'iwidget_applianceoperation')

        # Deleting model 'Country'
        db.delete_table(u'iwidget_country')

        # Deleting model 'UserProfile'
        db.delete_table(u'iwidget_userprofile')

        # Deleting model 'UserValidationKey'
        db.delete_table(u'iwidget_uservalidationkey')

        # Deleting model 'UserNotifications'
        db.delete_table(u'iwidget_usernotifications')


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
        u'iwidget.appliance': {
            'Meta': {'object_name': 'Appliance'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appliances'", 'to': u"orm['tl.Brand']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appliances'", 'to': u"orm['iwidget.Household']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'})
        },
        u'iwidget.applianceoperation': {
            'Meta': {'object_name': 'ApplianceOperation'},
            'appliance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['iwidget.Appliance']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'iwidget.appliancetimeseries': {
            'Meta': {'ordering': "('hidden',)", 'object_name': 'ApplianceTimeseries', '_ormbases': [u'hcore.Timeseries']},
            'appliance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeseries'", 'to': u"orm['iwidget.Appliance']"}),
            u'timeseries_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Timeseries']", 'unique': 'True', 'primary_key': 'True'})
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
        u'iwidget.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'})
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
        u'iwidget.iwtimeseries': {
            'Meta': {'ordering': "('hidden',)", 'object_name': 'IWTimeseries', '_ormbases': [u'hcore.Timeseries']},
            'regular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'timeseries_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Timeseries']", 'unique': 'True', 'primary_key': 'True'}),
            'typical': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        u'iwidget.smartmeter': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SmartMeter', '_ormbases': [u'hcore.Instrument']},
            u'instrument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hcore.Instrument']", 'unique': 'True', 'primary_key': 'True'}),
            'precision': ('django.db.models.fields.IntegerField', [], {'default': '5', 'blank': 'True'}),
            'specs': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'iwidget.usernotifications': {
            'Meta': {'object_name': 'UserNotifications'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detected': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notification': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remark': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': u"orm['auth.User']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'iwidget.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['iwidget.Country']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'iwidget.uservalidationkey': {
            'Meta': {'object_name': 'UserValidationKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'popup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sso': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'validation_key'", 'to': u"orm['auth.User']"})
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
        u'tl.brand': {
            'Meta': {'ordering': "('descr',)", 'object_name': 'Brand'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tl.Technology']"})
        },
        u'tl.technology': {
            'Meta': {'object_name': 'Technology'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'frequency_of_use_default': ('django.db.models.fields.FloatField', [], {'default': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['iwidget']