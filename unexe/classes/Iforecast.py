'''
Created on 5 Apr 2014

@author: adeel
'''
import datetime, json
from py4j.java_gateway import JavaGateway, GatewayClient
from Iseries import iseries
from Iutility import iutility
from Ihousehold import ihousehold
from iwidget.models import *

class iforecast():
    def __init__(self,javats,unitcost=1.0):
        self.ts = javats
        self.unitcost = unitcost #unit cost

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
                         
    #yearly forecasting using multi-layer perceptrols
    def getForecast(self,tseries,units,algorithm,file,default="year"):
        highest  = 0.0
        lowest   = 0.0
        billdata = {"sum":0.0,"avg":0.0,"high":"","low":""}
        dtlist = []
        list2  = []
        list1  = []
        data = {}       
        hhold    = ihousehold()
        series   = iseries()
        
        enddate  = series.getfinaldate(tseries) #end date of the time series
        #file = self.ts.getyearlyArff()

        if algorithm=="mlp":
            result = self.ts.getForecast(file,units,self.ts.getMLP(),"cost") #execute forecast using MLP for 12 units in future
        elif algorithm=="lr": 
            result = self.ts.getForecast(file,units,self.ts.getLinear(),"cost") #execute forecast using MLP for 12 units in future
        elif algorithm=="gr": 
            result = self.ts.getForecast(file,units,self.ts.getGaussian(),"cost") #execute forecast using MLP for 12 units in future
        else:
            return None
                   
        list2 = result.split(',') #get result in list
        
        if default=="days":
            for x in range(0,units):
                dt = str(enddate + datetime.timedelta(days=(x+1)))
                dtlist.append(dt)
                
        else:
            #get all future dates in list
            for x in range(0, units):
                dt = str(iutility.addMonths(enddate,x+1)) 
                dtlist.append(dt)
                cost = round(hhold.tariff1(float(list2[x])),2)
                list1.append(cost)
                billdata["sum"] = billdata["sum"] + cost
                #list1.append(iutility.getDate(dt,'%Y-%m-%d','%d-%m-%Y')) #covert format from YYY-mm-dd to dd-mm-YYYY
        
        highest = max(list1)
        lowest  = min(list1)    
        billdata["sum"]  = round(billdata["sum"],2)
        billdata["avg"]  = round(billdata["sum"]/units,2)
        billdata["high"] = {"date":iutility.convertdate(dtlist[list1.index(highest)],'%Y-%m-%d','%B-%Y'),"max":highest} #max per nonth
        billdata["low"]  = {"date":iutility.convertdate(dtlist[list1.index(lowest)],'%Y-%m-%d','%B-%Y'),"min":lowest} #min per nonth
        
        data["data"]     = series.getlistTojsoncost(dtlist,list1,"Date","Cost")  #merge two list for passing to client for charting
        data["billdata"] = billdata        
        data["title"]    = "NEXT "+ str(units) +" MONTHS BILL FORECAST"        
        
        '''
        price break lines
        '''
        start = dtlist[0]
        end   = dtlist[units-1]
        data["price_break"] = [
                       { "Price Break" : "Highest", "Cost" : highest, "Date" : start }, 
                       { "Price Break" : "Highest", "Cost" : highest, "Date" : end },
                       { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : start }, 
                       { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : end },
                       { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : start }, 
                       { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : end }
                   ];  
                           
        try:
            ""#entry.shutGateway()
        except:
            pass
        
        #data=""
        return data
    
    def getSum(self,json):
        sum = 0.0
        for d in json:
            sum = sum + float(d['cost'])
        return sum

    def getAvg(self,json,months):
        avg = self.getSum(json)/months
        return avg

    def getHighest(self,json):
        high = 0.0
        obj = {}
        for d in json:
            if float(d['cost']) > high:
                high = float(d['cost'])
                obj = {}
                obj["date"] = d["date"]
                obj["cost"] = d["cost"]
        return obj

    def getHighestCost(self,json):
        high = 0.0
        obj = {}
        for d in json:
            if float(d['cost']) > high:
                high = float(d['cost'])
                obj = {}
                obj["date"] = d["date"]
                obj["cost"] = d["cost"] * self.unitcost
        return obj
    
    def getLowest(self,json):
        low = 0.0
        count=0
        obj = {}
        for d in json:
            if count==0:
                low = float(d['cost'])
                obj["date"] = d["date"]
                obj["cost"] = d["cost"]                
            else: 
                if float(d['cost']) < low:
                    low = float(d['cost'])
                    obj = {}
                    obj["date"] = d["date"]
                    obj["cost"] = d["cost"]
            count = count + 1
        return obj

    def getLowestCost(self,json):
        low = 0.0
        count=0
        obj = {}
        for d in json:
            if count==0:
                low = float(d['cost'])
                obj["date"] = d["date"]
                obj["cost"] = d["cost"] * self.unitcost                
            else: 
                if float(d['cost']) < low:
                    low = float(d['cost'])
                    obj = {}
                    obj["date"] = d["date"]
                    obj["cost"] = d["cost"] * self.unitcost
            count = count + 1
        return obj    