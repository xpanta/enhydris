'''
Created on 13 Mar 2014

@author: adeel
'''

from django.core import serializers
import json

'''
This class serialize the python objects, mainly database objects and return serializable to be used at client side.
'''
class iserialize():    
    
    '''
    result: django queryset. Empty queryset will also be serialize and needs to be handled at client side
    column: It is the database column names that will be serialize
    '''
    def modelToJSON(self,result,column):
        data = serializers.serialize('json',result,fields=(column)) 
        return json.loads(data)