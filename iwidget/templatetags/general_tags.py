# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2014 National Techincal University of Athens

from django import template

register = template.Library()

@register.filter('getfor')                                                                
def getfor(obj, arg):                                                                     
    """                                                                                   
    Returns the value of the key ``arg`` from the dictionary ``obj``, or the              
    attribute ``arg`` of the object ``obj``                                               
    """                                                                                   
    if hasattr(obj, 'has_key') and obj.has_key(arg):                                      
        return obj.get(arg)                                                               
    arg = str(arg)                                                                        
    if hasattr(obj, arg):                                                                 
        return getattr(obj, arg)                                                          
    return None       
