'''
Created on 07 Mar 2014
@author: adeel
'''
import datetime
#from datetime import timedelta
import calendar

'''
Utility class contains the general purpose methods that include from reading values from
HTTP request object to date manupulation. All methods are static
'''
class iutility():

    '''
    This methods return value from querystring (qs) using POST
    request: HTTP request object 
    key    : it is the key to get the value from qs - form control DOM id
    return : any value from the quertstring as (String) if wrong key then return False (Boolean). 
        >>> def post(self, request, *args, **kwargs):
        >>>     iutility.getPostValue("key",request)    
    '''    
    @staticmethod
    def getPostValue(key,request):
        if(request.POST.has_key(key)):
            return request.POST.get(key)
        else:
            return False
    
    '''
    This methods return value from querystring (qs) using GET
    request: HTTP request object 
    key    : it is the key to get the value from qs - form control DOM id
    return : any value from the quertstring as (String) if wrong key then return False (Boolean).
        >>> def get(self, request, *args, **kwargs):
        >>>     iutility.getGetValue("key",request)    
    '''  
    @staticmethod
    def getGetValue(key,request):
        if(request.GET.has_key(key)):
            return request.GET.get(key)
        else:
            return False    

    '''
    This status methods get the querystring from the POST request
    '''
    @staticmethod
    def getPostqs(request):
        return request.POST.urlencode().encode('ASCII')
    
    '''
    This statis methods get the querustring from the GET request
    request: HTTP request object 
    return : Key, value pair from the querystring
    '''
    @staticmethod
    def getGetqs(request):
        return request.GET.urlencode().encode('ASCII')        


    '''
    convert string into date object
    #dt: date string
    #fmt: date format
    #return: date object
        >>> iutility.getstrTodate("2010-02-01","%Y-%m-%d")
        >>> date(2010,02,01)
    '''
    @staticmethod
    def getstrTodate(dt,fmt):
        return datetime.datetime.strptime(dt, fmt).date()
    
    '''
    This method convert date string one format to another format
    input: format to convert from
    output: desired date format
    dt is a date string
    return: desired output format (string)
    see datetime python library for further details
    see srptime for different format support
        >>> iutility.convertdate("2014-12-01",'%Y-%m-%d','%d-%m-%Y')
        >>> 01-12-2014
    '''
    @staticmethod
    def convertdate(dt,input,output):
        return datetime.datetime.strptime(dt, input).strftime(output)

    """
    Return a last day of the month as `datetime` or `datetime`.
    date: date object
        >>> last_day_month(datetime.date(2010, 4, 1))
        datetime(2010, 4, 30,0,0)
    """ 
    @staticmethod
    def last_day_month(date):
        next_month = date.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)        
    
    """
    Return a `datetime.date` or `datetime.datetime` (as given) that is
    month or year before .
    
        >>> subtract_one_month(datetime.date(2010, 4, 1),month="3")
        datetime.date(2010, 1, 1)
        >>> subtract_one_month(datetime.date(2010, 4, 1),year=1,month="3")
        datetime.date(2009, 1, 1)
    """ 
    @staticmethod
    def subtract_year_month(date, year=0, month=0):
        year, month = divmod(year*12 + month, 12)
        if date.month <= month:
            year = date.year - year - 1
            month = date.month - month + 12
        else:
            year = date.year - year
            month = date.month - month
        return date.replace(year = year, month = month)

    '''
    get number of days between 2 dates
    d1: first date (datetime object)
    d2: second date (datetime object)
    return number of months
         >>>iutility.diffdays(datetime.date(2012,09,16),datetime.date(2012,10,18))
         >>> 1
    '''
    @staticmethod
    def diffdays(d2, d1):
        delta = d2 - d1
        return delta.days
    
    '''
    get difference of months between 2 dates
    d1: first date (datetime object)
    d2: second date (datetime object)
    return number of months
         >>> iutility.diffmonth(datetime.date(2012,08,18),datetime.date(2012,09,18))
         >>> 1
    '''
    @staticmethod
    def diffmonth(d1, d2):
        return (d1.year - d2.year)*12 + d1.month - d2.month
        
    '''
    This method add months to the datetime object
    #curdate: it is the date object
    #months: No of months to add
    return: date after adding months
    '''
    @staticmethod
    def addMonths(curdate,months):
        month = curdate.month - 1 + months
        year  = curdate.year + month / 12
        month = month % 12 + 1
        day   = min(curdate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)