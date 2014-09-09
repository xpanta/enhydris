'''
Created on 01 Apr 2014

@author: adeel
'''
import json, datetime, math
from django.db import connection
from Iutility import iutility
from iwidget.models import (TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY, TSTEP_MONTHLY,VAR_CUMULATIVE, VAR_PERIOD, VAR_COST, TSTEP_HOURLY)
from pthelma.timeseries import Timeseries
from enhydris.hcore.models import ReadTimeStep

class iseries():
    def __init__(self,unitcost=1.0):
        #unit cost
        self.unitcost = unitcost

    '''
    This method sets the unit cost
    cost: the unit cost 
    '''    
    def setCost(self,cost):
        self.unitcost = cost
        
    '''
    This method calculate the cost per unit
    #data: total units obtained from timeseries data
    return: cost of the bill 
    '''    
    def getCost(self,data):
        return data * self.unitcost
    
    #data: time series list (date,units) obtained from pthemla timeseries
    #month: number of months to take average, deault is 12
    def getAvg(self,data,months):
        avg = self.getSum(data)/months
        return avg
        
    #data: time series list (date,units) obtained from pthemla timeseries
    #return: sum of units
    def getSum(self,data):
        sum = 0.0
        for d in data:
            if math.isnan(d[1]):
                continue
            sum = sum + d[1]

        return sum

    #date: time series list (date,units) obtained from pthemla timeseries
    #return: json object of highest value and date 
    def getHighest(self,data):
        high = 0.0
        obj = {}
        list = ['dump'] 
        for d in data:
            if math.isnan(d[1]):
                continue 
            if high < d[1]:
                high = d[1] #value
                dt = str(d[0].date()) #date
                dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                obj["date"] = dt
                obj["unit"] = high  
                list[0] = obj
                obj     = {};

        #if all the values in the series is NAN 
        if list[0]=="dump":
            obj["date"] = ""
            obj["unit"] = 0.0
            list[0]     = obj
                
        return list

    #date: time series list (date,units) obtained from pthemla timeseries
    #return: json object of highest value and date 
    def getHighestCost(self,data):
        high = 0.0
        obj  = {}
        list = ['dump'] 
        for d in data:
            if math.isnan(d[1]):
                continue 
            if high < d[1]:
                high = d[1] #value
                dt   = str(d[0].date()) #date
                dt   = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                obj["date"] = dt
                obj["cost"] = high * self.unitcost  
                list[0] = obj
                obj     = {};

        #if all the values in the series is NAN 
        if list[0]=="dump":
            obj["date"] = ""
            obj["cost"] = 0.0
            list[0]     = obj
                
        return list
    
    #date: time series list (date,units)
    #return: json object of lowest value and date 
    def getLowest(self, data):
        count=0
        low = 0.0
        obj = {}
        list = ['dump']         
        for d in data:
            if math.isnan(d[1]):
                continue            
            if count==0:
                low = d[1]
                dt = str(d[0].date()) #date
                dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                obj["date"] = dt
                obj["unit"] = low
                list[0] = obj
                obj = {};                
            else:
                if d[1] < low:
                    low = d[1]
                    dt = str(d[0].date()) #date
                    dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                    obj["date"] = dt
                    obj["unit"] = low  
                    list[0] = obj
                    obj = {};                    
            count = count + 1
        
        #if all the values in the series is NAN 
        if list[0]=="dump":
            obj["date"] = ""
            obj["unit"] = 0.0
            list[0] = obj
            
        return list

    #date: time series list (date,units)
    #return: json object of lowest value and date 
    def getLowestCost(self, data):
        count=0
        low = 0.0
        obj = {}
        list = ['dump']         
        for d in data:
            if math.isnan(d[1]):
                continue            
            if count==0:
                low = d[1]
                dt = str(d[0].date()) #date
                dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                obj["date"] = dt
                obj["cost"] = low  * self.unitcost
                list[0] = obj
                obj = {};                
            else:
                if d[1] < low:
                    low = d[1]
                    dt = str(d[0].date()) #date
                    dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%y') #covert format from YYY-mm-dd to dd-mm-YYYY
                    obj["date"] = dt
                    obj["cost"] = low * self.unitcost  
                    list[0] = obj
                    obj = {};                    
            count = count + 1
        
        #if all the values in the series is NAN 
        if list[0]=="dump":
            obj["date"] = ""
            obj["cost"] = 0.0
            list[0] = obj
            
        return list
       
    '''
    This method takes python list of dates and values and return json object to be used to display chart on client side
    #list1: list of dates strings
    #list2: list of values strings
    #key1: key name of date list
    #key2: key name of values list
    return json object to be used to send to client to display graph
    '''
    def getlistTojson(self,list1,list2,key1,key2):
        obj = {};
        dlist = []        
        for l1,l2 in zip(list1, list2):
            obj[key1] = str(l1)
            obj[key2]  = float(l2)
            dlist.append(obj)
            obj = {};
            
        return dlist

    '''
    This method takes python list of dates and values and return json object to be used to display chart on client side
    #list1: list of dates strings
    #list2: list of values strings
    #key1: key name of date list
    #key2: key name of values list
    return json object to be used to send to client to display graph
    '''
    def getlistTojsoncost(self,list1,list2,key1,key2):
        obj = {};
        dlist = []        
        for l1,l2 in zip(list1, list2):
            obj[key1] = l1
            obj[key2]  = float(l2) * self.unitcost
            dlist.append(obj)
            obj = {};
            
        return dlist

    '''
    This method takes python list of dates and values and return json object to be used to display chart on client side
    #list1: list of dates strings
    #list2: list of values strings
    #key1: key name of date list
    #key2: key name of values list
    #key3
    return json object to be used to send to client to display graph
    '''
    def getlistTojsoncost1(self,list1,list2,key1,key2):
        obj = {};
        dlist = []        
        for l1,l2 in zip(list1, list2):
            obj[key1] = l1
            obj[key2]  = float(l2) * self.unitcost
            dlist.append(obj)
            obj = {};
            
        return dlist
            
    '''
    this method returns the latest date from the timeseries
    tseries: timeseries object
    return latest date object
    '''
    def getfinaldate(self,tseries):
        length = len(tseries) #get length of time series
        dt = tseries[length-1] #fetch the last element which is the end date (datetime object)
        return dt[0].date() #datetime
        
    '''    
    this methods convert timeseries obtained from data to json
    tseries: timeseries object
    col: default value of json column that will be used for calculation and/or showing results. this is usually a unit
    return json formatted
    '''
    def getseriesTojson(self,tseries,col="unit"):
        obj = {}
        list1 = []
        num = 0.0
        for d in tseries:
            obj["date"] = str(d[0].date())
            num         = float(d[1])
            if math.isnan(num): # i have to do this so forecasting can take place - with NaN weka forecasting plugin throw exception
                num = 0.0
            obj[col] = num
            list1.append(obj)
            obj = {};
            
        return list1        

    '''    
    this methods convert timeseries obtained from data to json
    tseries: timeseries object
    col: default value of json column that will be used for calculation and/or showing results. this is usually a unit
    return json formatted
    '''
    def getseriesToelectricjson(self,tseries,quota,col="unit"):
        obj = {}
        list1 = []
        num = 0.0
        for d in tseries:
            obj["date"] = str(d[0].date())
            num         = float(d[1])
            if math.isnan(num): # i have to do this so forecasting can take place - with NaN weka forecasting plugin throw exception
                num = 0.0
            
            if num>0.0:
                num = iutility.percentage(num,quota)
            
            obj[col] = num
            list1.append(obj)
            obj = {};
            
        return list1 
    
    '''    
    this methods convert timeseries obtained from data to json
    tseries: timeseries object
    col: default value of json column that will be used for calculation and/or showing results
    return json formatted
    '''
    def getseriesTojsoncost(self,tseries,col="cost"):
        obj = {};
        list = []
        for d in tseries:
            #dt = str(d[0].date())
            #dt = iutility.convertdate(dt,'%Y-%m-%d','%d-%m-%Y')
            #reading = d[1] 
            obj["date"] = str(d[0].date())
            obj[col] = d[1] * self.unitcost
            list.append(obj)
            obj = {};
            
        return list 

    #this method returns daily timeseries
    #household: household object
    def gethourlyseries(self,household):
        return household.timeseries.filter(
            time_step__id=TSTEP_HOURLY,
            variable__id=VAR_PERIOD)[0]
    
    '''        
    this method returns daily timeseries
    household: household object
    '''
    def getdailyseries(self,household):
        return household.timeseries.filter(
            time_step__id=TSTEP_DAILY,
            variable__id=VAR_PERIOD)[0]
    
    '''             
    this method returns monthly timeseries
    household: household object
    months: number of months of timeseries to return (end of months) - 0 or default means all months
        >>> user       = request.user #get authenticated user
        >>> household  = user.households.all()[0] #get user household id
        >>> series     = iseries()
        >>> ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
    '''
    def getmonthlyseries(self,household):
        return household.timeseries.filter(time_step__id=TSTEP_MONTHLY,variable__id=VAR_PERIOD)[0]

    '''             
    this method return the number of months of data from timeseries 
    household: household object
    months: number of months of timeseries to return (end of months)
    return: Number of months of timeseries object (last months) or None if months are less
        >>> user       = request.user #get authenticated user
        >>> household  = user.households.all()[0] #get user household id
        >>> series     = iseries()
        >>> ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
        >>> return series.getseriesmonths(ts_monthly,3)
    '''
    def getseriesmonths(self,timeseries,months):
        if len(timeseries)>=months:
            return timeseries[len(timeseries)-months:]
        else:
            None
                        
    #this method read time step
    #timeseries: this is the time series object
    def readseries(self,timeseries):
        time_step  = ReadTimeStep(timeseries.id, timeseries)
        timeseries = Timeseries(time_step=time_step,id=timeseries.id)
        timeseries.read_from_db(connection)
        return timeseries.items()
    
    '''
    This method is use to find from timeseries the start date
    timeseries: this is the time series that has all values and datetime from start to finish
    return: python date object 
        >>> ts_daily = series.getdailyseries(household)
        >>> timeseries_daily = series.readseries(ts_daily)
        >>> series.getstdate(timeseries_daily)
    '''
    def getstdate(self,timeseries):
        dt = timeseries[0]
        return dt[0].date()

    '''
    This method is use to find from timeseries the end date
    timeseries: this is the time series that has all values and datetime from start to finish
    return: python date object 
        >>> ts_daily = series.getdailyseries(household)
        >>> timeseries_daily = series.readseries(ts_daily)
        >>> series.getendate(timeseries_daily)
    '''
    def getendate(self,timeseries):
        dt = timeseries[len(timeseries)-1]
        return dt[0].date()