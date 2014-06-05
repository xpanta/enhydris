#UWOTTL, Copyright (c) 2012, National Technical University of Athens
#This script is used to import the initial data from the
#../data directory to the database file

import os
from django.core.exceptions import ObjectDoesNotExist as e1
from django.core.exceptions import MultipleObjectsReturned as e2
from uwottl.tl.models import *

DATAPATH = '/home/soulman/uwottl/data/'

def run():

    print 'Importing units'
    with open(os.path.join(DATAPATH, 'unit.csv')) as f:
        for line in f:
            (id, descr) = line.split('\t',1)
            unit = Unit(id=int(id), descr=descr.strip())
            unit.save()

    print 'Importing categories'
    with open(os.path.join(DATAPATH, 'category.csv')) as f:
        for line in f:
            (id, descr) = line.split('\t',1)
            category = SpecificationCategory(id=int(id),
                                             descr=descr.strip())
            category.save()

    print 'Importing technologies'
    with open(os.path.join(DATAPATH, 'technology.csv')) as f:
        for line in f:
            (id, code, descr) = line.split('\t',2)
            technology = Technology(id=int(id), descr=descr.strip(), 
                                    code=code.strip(), remarks='')
            technology.save()

    print 'Importing brands'
    with open(os.path.join(DATAPATH, 'brand.csv')) as f:
        for line in f:
            (tech_id, brand_id, descr) = line.split('\t',2)
            brand = Brand(old_id=int(brand_id), descr= descr.strip(),
                          technology=Technology.objects.get(pk=tech_id))
            brand.save()

    print 'Importing specifications'
    with open(os.path.join(DATAPATH, 'specification.csv')) as f:
        for line in f:
            try:
                (id, tech_id, brand_id, no, i, j, category, value, 
                 unit) = line.split('\t',8)
                specification = Specification(no=no, i=i, j=j, 
                                              value=float(value))
                specification.category =\
                    SpecificationCategory.objects.get(pk=category)
                specification.brand = Brand.objects.get(old_id=brand_id,
                                                    technology=tech_id)
                unit = int(unit.strip())
                specification.unit = None if unit==-1 else\
                                     Unit.objects.get(pk=unit)
                specification.save()
            except e1, e2:
                print 'Error in id=%s, brand_id=%s, tech_id=%s'%(id,
                     brand_id, tech_id)
                      

            


