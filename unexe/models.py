from iwidget.models import *

'''
This model keep contains the location of arff file per user
that is used to forecast the next water bill using the 
JAVA weka forecasting library
'''

class Forecast(models.Model):
    yearfile  = models.CharField(max_length=100,blank=True)
    dailyfile = models.CharField(max_length=100,blank=True)
    yeardate  = models.DateField(blank=True,null=True)
    dailydate = models.DateField(blank=True,null=True)
    user      = models.ForeignKey(User,unique=True)


class ElectricForecast(models.Model):
    yearfile  = models.CharField(max_length=100,blank=True)
    dailyfile = models.CharField(max_length=100,blank=True)
    yeardate  = models.DateField(blank=True,null=True)
    dailydate = models.DateField(blank=True,null=True)
    user      = models.ForeignKey(User,unique=True)
        
class BaseDMAstats(models.Model):
    statsdate     = models.DateField(auto_now=True)
    statsperiod   = models.PositiveSmallIntegerField()
    sumhouseholds = models.PositiveIntegerField()
    sumoccupants  = models.PositiveIntegerField()
    sumunits      = models.FloatField()
    maxunits      = models.FloatField()
    avgunits      = models.FloatField()
    minunits      = models.FloatField()
    household     = models.ForeignKey(Household)

    class Meta:
        abstract  = True

class userDMAstats(BaseDMAstats):
    options       = models.PositiveSmallIntegerField() # This field indicate the statistics type,1=num of occupants, 2=property type, 3=number of occupants+property type

class DMAstats(models.Model):
    statsdate     = models.DateField(auto_now=True)
    statsperiod   = models.PositiveSmallIntegerField()
    sumhouseholds = models.PositiveIntegerField()
    sumoccupants  = models.PositiveIntegerField()
    sumunits      = models.FloatField()
    maxoccupants  = models.PositiveIntegerField()
    avgoccupants  = models.PositiveIntegerField()
    minoccupants  = models.PositiveIntegerField()
    maxunits      = models.FloatField()
    avgunits      = models.FloatField()
    minunits      = models.FloatField()
    dma           = models.ForeignKey(DMA)


class Ediary(models.Model):
    diary_ts = models.DateTimeField()
    diary_entry = models.TextField()
    hh_ref = models.ForeignKey(Household)