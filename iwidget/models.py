# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Techincal University of Athens

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from enhydris.hcore.models import (Lookup as HLookup, Timeseries, Gpoint,
                                   Garea, Instrument)
from tl.models import Brand

# These are the ids of Timestep Objects in db. Timestep entities
# are initialized with a creation script

TSTEP_FIFTEEN_MINUTES = 1
TSTEP_DAILY = 2
TSTEP_MONTHLY = 3
TSTEP_HOURLY = 4

# Same for variables and timezone

VAR_CUMULATIVE = 1
VAR_PERIOD = 2
VAR_COST = 3
VAR_COLD_PERIOD = 4
VAR_HOT_PERIOD = 5
VAR_ENERGY_PERIOD = 6
VAR_COLD_CUMULATIVE = 7
VAR_HOT_CUMULATIVE = 8
VAR_ENERGY_CUMULATIVE = 9
VAR_ENERGY_COST = 10

TZONE_UTC = 1

# Units

CUBIC_METERS = 1
UNIT_EURO = 2
UNIT_KILOWATTHOUR = 3

# alternative ID, based on Water company id

GENTITYALTCODETYPE = 1


class Lookup(HLookup):
    """
    We change ordering -> id
    """
    pass
    
    class Meta:
        abstract = True
        ordering = ('id',)

class DMA(Garea):
    """
    The DMA class inherits from Garea gentity type.
    DMA is a District Management Area containing many households
    """
    description = models.CharField(max_length=45)
    socio_demographics = models.TextField()
    location = models.CharField(max_length=45)

class PropertyType(Lookup):
    """
    Property type is a simple lookup with descr field, no extra
    definitions needed"""
    pass

class ConstructionPeriod(Lookup):
    pass

class OwnershipStatus(Lookup):
    pass

class OutdoorFacility(Lookup):
    pass

class WaterHeater(Lookup):
    pass

class WaterPricingScheme(Lookup):
    pass

class EfficientAppliance(Lookup):
    pass

class WaterDMS(Lookup):
    pass

class HouseholdValueCategory(Lookup):
    pass

class HouseholdValueSubcategory(Lookup):
    category = models.ForeignKey("HouseholdValueCategory",
            related_name='subcategories')
    form_component = models.CharField(max_length=45, blank=True,
            null=True)

class ArithmeticValueItem(models.Model):
    subcategory = models.ForeignKey("HouseholdValueSubcategory")
    household = models.ForeignKey("Household",
            related_name="arithmetic_values_items")
    number = models.IntegerField()

    class Meta:
        unique_together = ('subcategory', 'household')

class Household(Gpoint):
    """
    Household is also a Gentity of Gpoint type, described spatially by
    a single point. Household can be part of one only DMA and owned by
    a single database user with the appropriate Foreign Keys.
    """
    num_of_occupants = models.IntegerField(null=True,
            verbose_name = 'Number of occupants',
            help_text = 'The total number of occupants living in the '
                        'household')
    address = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, related_name='households')
    property_type = models.ForeignKey(PropertyType, null=True,
            blank=True,
            help_text='specify to which category your house belongs')
    property_size = models.FloatField(blank=True, null=True,
            verbose_name=u'Size of property in m²')
    dma = models.ForeignKey(DMA, related_name='households')
    neighbours = models.ManyToManyField("self", symmetrical=False,
            through='Neighbour')
    arithmetic_values = models.ManyToManyField(
            "HouseholdValueSubcategory",
            through="ArithmeticValueItem")
    construction_period = models.ForeignKey('ConstructionPeriod',
            verbose_name='Period of construction',
            help_text='specify to which category your house belongs',
            blank=True, null=True)
    ownership_status = models.ForeignKey('OwnershipStatus',
            verbose_name='Ownership status',
            blank=True, null=True)
    outdoor_facilities = models.ManyToManyField(
            "OutdoorFacility",
            verbose_name="Outdoor facilities",
            help_text="mark the outdoor facilities of your house$",
            blank=True)
    water_heaters = models.ManyToManyField(
            "WaterHeater",
            verbose_name="How the water is heated at your house?",
            help_text="Mark all the heating systems used$",
            blank=True)
    water_pricing = models.ForeignKey('WaterPricingScheme',
            verbose_name='Specify the type of water pricing scheme of '
                         'your household',
            blank=True, null=True)
    efficient_appliances = models.ManyToManyField(
            "EfficientAppliance",
            verbose_name="Which of the following water efficient "
                         "appliance do you have at your house?",
            help_text="Mark the appliances$",
            blank=True)
    water_dms = models.ManyToManyField(
            "WaterDMS",
            verbose_name="Do you have innovative water demand "
                         "management systems?",
            help_text="Mark the systems$",
            blank=True)

    def get_absolute_url(self):
        return reverse('household_view', kwargs={'household_id':
            self.id})

class Neighbour(models.Model):
    """
    This is a relation that connects two households to form a
    neighbour, household1 and household2. (household1, household2) are
    unique together by adding the proper database constraint.
    This relation defines a ManyToMany constraint between Household
    entities.
    Later extra fields can be added to a "Neighbour" relation.
    """
    household1 = models.ForeignKey("Household",
            related_name='household1')
    household2 = models.ForeignKey("Household",
            related_name='household2')

    class Meta:
        unique_together = (('household1', 'household2'),)

class IWTimeseries(Timeseries):
    """
    This is a special case of Timeseries class for the iWidget
    application. IWTimeseries is a subclass of Timeseries inherits all
    Timeseries properties and add some extra.
    IWTimeseries may have FK (Nullable) to SmartMeters via instrument
    FK.
    Instrument is modified by changing the FK to station relation to
    NULL since stations are not used in general in iWidget
    applications. For the reason a south migration script exists.
    """
    typical = models.BooleanField(default=False)
    regular = models.BooleanField(default=False)

class ApplianceTimeseries(Timeseries):
    """
    This is another subclass of time series, for time series related
    to an appliance with Foreign Key to Appliance NOT NULL
    """
    appliance = models.ForeignKey("Appliance", null=False,
            related_name="timeseries")

class SmartMeter(Instrument):
    """
    This is a class for SmartMeter objects subclassing the
    enhydris.hcore.Instrument class and representing smart meters that
    they can be attached to households. SmartMeter like Instrument can
    be connected with a Timeseries withe the Timeseries.instrument
    property that is a ForeignKey to the Instrument relations.
    Instrument is modified by changing the FK to station relation to
    NULL since stations are not used in general in iWidget
    applications. For the reason a south migration script exists.
    This is done with the south_migration entry 0003 for the iwidget
    application.
    """
    # Precision denotes the number of decimal digits, e.g. a default
    # value of 5: 12.12345
    precision = models.IntegerField(default = 5, blank=True)
    specs = models.CharField(max_length=45, blank=True)
    url = models.URLField(blank=True)

class Appliance(models.Model):
    """
    This is the class for a single Appliance. Appliance is
    characterized by a type called "brand" and connected with the
    Technological Library Brand class with Foreign Key constraint.
    """
    name = models.CharField(max_length=45, blank=True)
    description = models.CharField(max_length=45, blank=True)
    brand = models.ForeignKey(Brand, null=False, related_name="appliances")
    household = models.ForeignKey(Household,
            related_name="appliances")

class ApplianceOperation(models.Model):
    """
    This is a helper relation for the Appliance type with FK to
    appliance specifying an operation period. Operation period is
    defined with start and end timestamps (both nullable, since period
    can be open) and a scheduled boolean field.
    """
    appliance = models.ForeignKey("Appliance", null=False,
            blank=False, related_name="operations")
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    scheduled = models.BooleanField(default=False)

'''
'''
class Country(models.Model):
    name    = models.CharField(max_length=100)
    point   = models.PointField(geography=True,blank=True,null=True)
    polygon = models.MultiPolygonField(blank=True,null=True)
    
    objects = models.GeoManager()

'''
This is the user profile class. This class will store user profile details 
'''
class UserProfile(models.Model):
    address  = models.TextField() 
    user     = models.ForeignKey(User,unique=True)
    country  = models.ForeignKey(Country,blank=True,null=True)


"""
    Next model is added by Chris Pantazis on 15/Sept/2014.
    It will be used to store a unique key for each household user.
    This key along with the meter id (or something else) will be used
    together for the user to login and change username and password.

    UPDATE: After discussions, we decided to use the SSO for users to login.
    Therefore, the key becomes the password (stored in auth_user, too).
    I decided to keep it this way
    because it is easier for the developer to login as any user for testing
    reasons. Future devs should be aware of this small issue and stop using
    this key as password. Key is being updated when the user changes his/her
    password.

    From this table, only two fields are actually needed. The "sso" field that
    lets us know if the user is stored in SSO database (initially it is false,
    then if user is stored in SSO server by another scheduled process, it
    becomes True. And, secondly, popup which lets us know if the user has
    added extra details we need (if True, it shows a in-between screen that
    asks for name, email and occupants. If form is submitted this value becomes
    False and form is never displayed again).
"""


class UserValidationKey(models.Model):
    user = models.ForeignKey(User, related_name='validation_key')
    identifier = models.CharField(max_length=128, help_text="meter identifier")
    key = models.CharField(max_length=64)  # password in text
    used = models.BooleanField(default=False)  # not used, at the moment
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sso = models.BooleanField(default=False)  # user in SSO Service?
    popup = models.BooleanField(default=True)  # new user? (show popup)

"""
    Next model is added by Chris Pantazis in order to store and show
    user notification messages. This is a very simple implementation but I
    think it does the job. I decided against using a two-table implementation
    with foreign keys, etc for brevity and deadline reasons. Also, I decided
    not to use full message here as it is hard to translate. Just the type
    is enough. Message will be created in templates and then translated.
"""


class UserNotifications(models.Model):
    user = models.ForeignKey(User, related_name="notifications")
    notification = models.CharField(max_length=64)  # leakage, burst, etc
    detected = models.DateField()
    event_time = models.CharField(max_length=10, default=0)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=False)  # if user agrees with event
    read = models.BooleanField(default=False)  # if user has seen the message
    remark = models.CharField(max_length=128, default="")
    consumption = models.FloatField(default=0)


    def __unicode__(self):
        return self.user.username + " > " + self.notification

