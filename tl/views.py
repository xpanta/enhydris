#UWOTTL, Copyright (c) 2012, National Technical University of Athens

from django.http import HttpResponse
from models import Specification, Brand

def specification_list(request, *args, **kwargs):
    specs = {'queryset': Specification.objects.all().extra(order_by =\
                    ['brand__technology__id', 'brand__id', 
                      'category__id']),
    } 
    s=''
    lines=[]
    queryset = specs['queryset']
    for item in queryset:
        lines.append(','.join(str(x) for x in (item.id,
                     item.brand.technology.id,
                     item.brand.id, item.no,
                     item.i, item.j, item.category.id,
                     item.value, 
                     -1 if item.unit==None else item.unit.id)))
    s='\r\n'.join(lines)
    response = HttpResponse(s, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tech_specs.csv'
    response['Content-Length'] = len(s)
    response['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate, post-check=0, pre-check=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Wed, 11 Jan 1984 05:00:00 GMT'
    return response

def brand_list(request,  *args, **kwargs):
    brands = { 'queryset': Brand.objects.all().extra(order_by=\
                ['technology__id', 'old_id',])}
    s=''
    lines=[]
    queryset = brands['queryset']
    for item in queryset:
        lines.append(','.join(str(x) for x in (
                     item.technology.id, item.old_id, item.id)))
    s='\r\n'.join(lines)
    response = HttpResponse(s, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=brands.csv'
    response['Content-Length'] = len(s)
    response['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate, post-check=0, pre-check=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Wed, 11 Jan 1984 05:00:00 GMT'
    return response
