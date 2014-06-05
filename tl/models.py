#UWOTTL, Copyright (c) 2012, National Technical University of Athens

from django.db import models

class Lookup(models.Model):
    descr = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.descr

    class Meta:
        abstract = True
        ordering = ('descr',)

class Technology(Lookup):
    code = models.CharField(max_length=10)
    remarks = models.TextField(null=False, blank=True)
    frequency_of_use_default = models.FloatField(null=False,
                                                 blank=True,
                                                 default=1)

    class Meta:
        verbose_name_plural = 'technologies'
        permissions = (
            ("can_alter_remarks", "Can alter remarks"),
            )


class Brand(Lookup):
    technology = models.ForeignKey(Technology)
    old_id = models.IntegerField(blank=True, null=True)

class Unit(Lookup): pass

class SpecificationCategory(Lookup): 

    class Meta:
        verbose_name_plural = 'specification categories'

class Specification(models.Model):    
    category = models.ForeignKey(SpecificationCategory)
    brand = models.ForeignKey(Brand)
    no = models.IntegerField(default=1)
    i = models.IntegerField(default=1)
    j = models.IntegerField(default=1)
    value = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    
    def __unicode__(self):
        return "%s - no: %d i: %d j: %d"%(self.brand,
               self.no, self.i, self.j,)

    class Meta:
        unique_together = ("id", "no", "i", "j",)


