'''
Created on 12 Mar 2014
@author: adeel
'''
from Iserialize import iserialize
from iwidget.models import Household
from iwidget.models import *
from Idma import idma
from Iseries import iseries
from Iutility import iutility
import json, datetime
import pandas as pd
import itertools as IT
import numpy as np

'''
This is household class where methods related to gather household statistics is defined. 
'''
class ihousehold():
    
    def __init__(self):
        self.electric = 18 #percentage of electricity usage from water - according to research/white paper or other resources  - see D222 documentation
        #column of the household class as defined in table
        self.col = ['num_of_occupants','property_type','contruction_period']

    '''
    This method analyse the data and calculate the bills using different tariff schemes
    This is a temporary method and when the database schema detail will be provided all these
    tariff details will be added to the DB
    Values takes from the existence tariff provided by AGS
    '''
    def  tariff1df(self,df):
        fix_charge = 5.46 #fixed charges for pipe diameter <=15 mm
        vm_charge1 = 0.65 # defined in euros (0 to 5 m3)
        vm_charge2 = 0.98 # defined in euros (6 to 10 m3)
        vm_charge3 = 1.24 # defined in euros (11 to 20 m3)
        vm_charge4 = 1.70 # defined in euros (>20)
        
        
        #print df[(df["units"]>= 6.0) & (df["units"]<=10.0)]
        df1 = df[df["units"] < 5.0] * vm_charge1 + fix_charge
        df2 = df[(df["units"] >= 6.0) & (df["units"]<=10.0)]   * vm_charge2 + fix_charge
        df3 = df[(df["units"] >= 11.0) & (df["units"]<=20.0)]  * vm_charge3 + fix_charge
        df4 = df[(df["units"] >= 21.0) & (df["units"]<=30.0)]  * vm_charge4 + fix_charge

        '''
        TO DO: Merge the dataframe 
        '''
                
        return df
         
    '''
    This method analyse the data and calculate the bills using different tariff schemes
    This is a temporary method and when the database schema detail will be provided all these
    tariff details will be added to the DB
    Values takes from the existence tariff provided by AGS
    '''
    def  tariff1(self,units):
        fix_charge = 5.46 #fixed charges for pipe diameter <=15 mm
        vm_charge1 = 0.65 # defined in euros (0 to 5 m3)
        vm_charge2 = 0.98 # defined in euros (6 to 10 m3)
        vm_charge3 = 1.24 # defined in euros (11 to 20 m3)
        vm_charge4 = 1.70 # defined in euros (>20)
        
        data = None
        
        if units<5.0:
            data = fix_charge + units * vm_charge1
        elif units>=6.0 and units<=10.0:
            data = fix_charge + units * vm_charge2
        elif units>=11.0 and units<=20.0:
            data = fix_charge + units * vm_charge3
        else:
            data = fix_charge + units * vm_charge4
            
        return data

    '''
    This method analyse the data and calculate the bills using different tariff schemes
    This is a temporary method and when the database schema detail will be provided all these
    tariff details will be added to the DB
    '''
    def  tariff2(self,units):
        fix_charge = 7.46 #fixed charges for pipe diameter <=15 mm
        vm_charge1 = 0.75 # defined in euros (0 to 5 m3)
        vm_charge2 = 1.10 # defined in euros (6 to 10 m3)
        vm_charge3 = 1.50 # defined in euros (11 to 20 m3)
        vm_charge4 = 1.90 # defined in euros (>20)
        
        data = None
        
        if units<5.0:
            data = fix_charge + units * vm_charge1
        elif units>=6.0 and units<=10.0:
            data = fix_charge + units * vm_charge2
        elif units>=11.0 and units<=20.0:
            data = fix_charge + units * vm_charge3
        else:
            data = fix_charge + units * vm_charge4
            
        return data    
    
    def getWaterstats(self,loggeduser):
        '''
        Calculating household monthly cost and other statistics
        '''
        dic12 = {"period":"","sum_units":"","avg_units":"","unit_person":""}
        household  = loggeduser.households.all()[0]
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household) 
        timeseries_monthly = series.readseries(ts_monthly)
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
        pdf   =  pd.DataFrame(list(units),index=list(dates),columns=["units"]) #create pandas Series (time series using two different list for timeseries data analysis
        #last 12 months
        pdf12 = pdf.ix[-12:] #get last 12 months
        dic12["period"] = "12 Months"
        dic12["sum_units"] = round(np.sum(pdf12.values)-iutility.percentage(np.sum(pdf12.values),self.electric),2)
        dic12["avg_units"] = round(dic12["sum_units"]/12,2)
        dic12["unit_person"]= round(dic12["sum_units"]/household.num_of_occupants,2)
        #last 6 months
        dic6  = dic12.copy()
        pdf6  = pdf.ix[-6:] #get last 6 months
        dic6["period"] = "6 Months"
        dic6["sum_units"] = round(np.sum(pdf6.values)-iutility.percentage(np.sum(pdf6.values),self.electric),2)
        dic6["avg_units"] = round(dic6["sum_units"]/6,2)
        dic6["unit_person"] = round(dic6["sum_units"]/household.num_of_occupants,2)
        #last 4 months
        dic4  = dic12.copy()
        pdf4  = pdf.ix[-3:] #get last 6 months
        dic4["period"] = "3 Months"
        dic4["sum_units"] = round(np.sum(pdf4.values)-iutility.percentage(np.sum(pdf4.values),self.electric),2)
        dic4["avg_units"] = round(dic4["sum_units"]/3,2)
        dic4["unit_person"] = round(dic4["sum_units"]/household.num_of_occupants,2)
        #last 1 month
        pdf1  = pdf.ix[-1:] #get last 1 month
        dic1  = dic12.copy()
        dic1["period"]    = "1 Month"
        dic1["sum_units"] = round(np.sum(pdf1.values)-iutility.percentage(np.sum(pdf1.values),self.electric),2)
        dic1["avg_units"] = round(dic1["sum_units"],2)
        dic1["unit_person"] = round(dic1["sum_units"]/household.num_of_occupants,2)
        #combine all data
        data = {"year":dic12,"half":dic6,"quarter":dic4,"month":dic1}
        return data
        
    '''
    This method returns the last 12 months' electricity units and cost of the household. Data is return in a format supported to render chart in a client side (Chart)
    '''
    def getElectricstats(self,loggeduser):
        #iutility.percentage(100,self.electric)
        '''
        Calculating household monthly cost and other statistics
        '''
        dic12 = {"period":"","sum_units":"","avg_units":"","unit_person":""}
        household  = loggeduser.households.all()[0]
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household) 
        timeseries_monthly = series.readseries(ts_monthly)
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
        pdf   =  pd.DataFrame(list(units),index=list(dates),columns=["units"]) #create pandas Series (time series using two different list for timeseries data analysis
        #last 12 months
        pdf12 = pdf.ix[-12:] #get last 12 months
        dic12["period"] = "12 Months"
        dic12["sum_units"] = round(iutility.percentage(np.sum(pdf12.values),self.electric),2)
        dic12["avg_units"] = round(dic12["sum_units"]/12,2)
        dic12["unit_person"]= round(dic12["sum_units"]/household.num_of_occupants,2)
        #last 6 months
        dic6  = dic12.copy()
        pdf6  = pdf.ix[-6:] #get last 6 months
        dic6["period"] = "6 Months"
        dic6["sum_units"] = round(iutility.percentage(np.sum(pdf6.values),self.electric),2)
        dic6["avg_units"] = round(dic6["sum_units"]/6,2)
        dic6["unit_person"] = round(dic6["sum_units"]/household.num_of_occupants,2)
        #last 4 months
        dic4  = dic12.copy()
        pdf4  = pdf.ix[-3:] #get last 3 months
        dic4["period"] = "3 Months"
        dic4["sum_units"] = round(iutility.percentage(np.sum(pdf4.values),self.electric),2)
        dic4["avg_units"] = round(dic4["sum_units"]/3,2)
        dic4["unit_person"] = round(dic4["sum_units"]/household.num_of_occupants,2)
        #last 1 month
        pdf1  = pdf.ix[-1:] #get last 1 month
        dic1  = dic12.copy()
        dic1["period"]    = "1 Month"
        dic1["sum_units"] = round(iutility.percentage(np.sum(pdf1.values),self.electric),2)
        dic1["avg_units"] = round(dic1["sum_units"],2)
        dic1["unit_person"] = round(dic1["sum_units"]/household.num_of_occupants,2)
        #combine all data
        data = {"year":dic12,"half":dic6,"quarter":dic4,"month":dic1}
        return data        

    '''
    Analyse the night data (smart water meter data - timeseries) of the logged user (household)
    user:   logged user (See User object for details) - from this user a household can be obtained
    period: periods in terms of number of months
    stdate: The start date of period to analyse if period is specified in range
    endate: The end date of period to analyse if period is specified in range
    return: If no data exists for the specified period or dates then return None other return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getdaystats(user,12) #dma with household and period is 12 months
        or 
        >>> h.getdaystats(user,"days","10-02-01","10-05-01") #dma with household and period is 12 months    
    '''    
    def getdaystats(self,loggeduser,period=0,stdate=None,endate=None):        
        data = {}
        dtlist = []
        list1  = []        
        day    = ""
        night  = ""
        yourdata = {"max":"","min":"","sum":"","avg":"","occupant":""}
        #day,night = None, None
        count = 0
        sumnight = 0.0
        household = loggeduser.households.all()[0] #get user household id  
        series    = iseries()
        
        if str(period)=="days": #start and end date (period) is specified 
            sdate     = iutility.convertdate(stdate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            edate     = iutility.convertdate(endate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            today     = iutility.getstrTodate(edate,"%Y-%m-%d") 
            #edate     = iutility.last_day_month(iutility.getstrTodate(edate,"%Y-%m-%d"))
            numdays   = iutility.diffdays(iutility.getstrTodate(edate,"%Y-%m-%d"),iutility.getstrTodate(sdate,"%Y-%m-%d"))  #number of days
            period    = iutility.diffmonth(iutility.getstrTodate(edate,"%Y-%m-%d"),iutility.getstrTodate(sdate,"%Y-%m-%d")) + 1 #number of months
            start     = iutility.subtract_year_month(today,month=period-1) #graph start date - i remove -1
            end       = today      
            
        else:      #period is specfied in months
            '''
            extract the data specified in the perid from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
            '''
            #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value
            today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
            today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
            today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
            start = iutility.subtract_year_month(today,month=period-1)
            end   = today
                    

        '''
        Check timeseries for the existence of the specified period data 
        '''
        ts_monthly = series.getmonthlyseries(household)
        tsmonthly  = series.readseries(ts_monthly)
                             
        #get dates and values in a separate list
        dates, units = IT.izip(*tsmonthly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        
        '''
        extract the data specified in the perid from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
        '''
        #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value
        #today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
        #today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
        #today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
        firstday = iutility.subtract_year_month(today,month=period-1) #i remove -1
        lastday  = iutility.last_day_month(today)

        #print firstday
        #print lastday
        pdfmonth = pdf[firstday:lastday]  
        #print pdfmonth     
        months = pdfmonth.count()
        
        if months["units"]!=period: # data is less than required period    
            return None
        
        #hourly series            
        ts_hourly = series.gethourlyseries(household)
        tshourly = series.readseries(ts_hourly)
        #get dates and values in a separate list
        dates, units = IT.izip(*tshourly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        
        for x in range(period,0,-1): #decrement the loop so chart shows last the previoud month
            firstday = iutility.subtract_year_month(today,month=(x-1))
            lastday  = iutility.last_day_month(firstday)
            pdfmonth = pdf[firstday:lastday]                            
            #replace all NAN with 0.0 to avoid messing up JSON at the client side
            pdfmonth["units"].fillna(0.0,inplace=True)
            pdfnight = pdfmonth.between_time('07:00','17:00')
            
            #night values
            pdfnight = np.sum(pdfnight.values) # sum all values
            sumnight = sumnight + pdfnight #sum monthly value
                                                   
            dtlist.append(str(firstday))
            list1.append(pdfnight)                       
                    
        data = series.getlistTojson(dtlist,list1,"date","units")
        
        yourdata["sum"]  = np.sum(list1) # sum all values
        yourdata["avg"]  = yourdata["sum"]/period #month average
        yourdata["occupant"] = yourdata["sum"]/household.num_of_occupants #month average            
        data.append({"yourdata":yourdata})
        return data
      
    '''
    Analyse the night data (smart water meter data - timeseries) of the logged user (household)
    user:   logged user (See User object for details) - from this user a household can be obtained
    period: periods in terms of number of months
    stdate: The start date of period to analyse if period is specified in range
    endate: The end date of period to analyse if period is specified in range
    return: If no data exists for the specified period or dates then return None other return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getperiodstats(user,2008-02-01","2008-04-01")    
    '''        
    def getperiodstats(self,loggeduser,stdate=None,endate=None):        
        data = {}
        dtlist = []
        list1 = []        
        day   = ""
        night = ""
        yourdata = {"household":0.0,"occupant":0.0}
        #day,night = None, None
        count = 0
        idx = 0
        sumnight = 0.0
        household = loggeduser.households.all()[0] #get user household id  
        series    = iseries()
        value = 0.0
        #if str(period)=="days": #start and end date (period) is specified 
            #sdate     = iutility.convertdate(stdate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            #edate     = iutility.convertdate(endate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
        today     = iutility.getstrTodate(endate,"%Y-%m-%d") 
            #edate     = iutility.last_day_month(iutility.getstrTodate(edate,"%Y-%m-%d"))
        numdays   = iutility.diffdays(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d"))  #number of days
        period    = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1 #number of months
        start     = iutility.subtract_year_month(today,month=period-1) #graph start date
        end       = today      
        
        #else:      #period is specfied in months
            
            #extract the data specified in the perid from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
            
            #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value
            #today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
            #today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
            #today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
            #start = iutility.subtract_year_month(today,month=period-1)
            #end   = today            
            
        '''
        Check timeseries for the existence of the specified period data 
        '''
        ts_monthly = series.getmonthlyseries(household)
        tsmonthly  = series.readseries(ts_monthly)
                             
        #get dates and values in a separate list
        dates, units = IT.izip(*tsmonthly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        
        '''
        extract the data specified in the perid from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
        '''
        #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value
        #today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
        #today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
        #today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
        firstday = iutility.subtract_year_month(today,month=period-1)
        lastday  = iutility.last_day_month(today)

        pdfmonth = pdf[firstday:lastday]  
        months   = pdfmonth.count()
        if months["units"]!=period: # data is less than required period or not available in the required period
            return None
        
        #hourly series    
        '''        
        ts_hourly = series.gethourlyseries(household)
        tshourly = series.readseries(ts_hourly)
        #get dates and values in a separate list
        dates, units = IT.izip(*tshourly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        '''
        for x in range(period,0,-1): #decrement the loop so chart shows last the previoud month
            firstday = iutility.subtract_year_month(today,month=(x-1))
            lastday  = iutility.last_day_month(firstday)
            #pdfmonth = pdf[firstday:lastday]                            
            #replace all NAN with 0.0 to avoid messing up JSON at the client side
            pdfmonth["units"].fillna(0.0,inplace=True)
            #pdfnight = pdfmonth.between_time('18:00','06:00')
            
            #night values
            #value = pdfmonth["units"][idx]   #np.sum(pdfnight.values) # sum all values
            #sumnight = sumnight + pdfnight #sum monthly value
                                                   
            dtlist.append(str(firstday))
            list1.append(round(pdfmonth["units"][idx],2))                       
            idx = idx + 1
     
        data["data"]         = series.getlistTojson(dtlist,list1,"date","units")
        yourdata["household"]= round(np.sum(list1),2) # sum all values
        #yourdata["avg"]      = yourdata["household"]/period #month average
        yourdata["occupant"] = round(yourdata["household"]/household.num_of_occupants,2) #month average            
        data["yourdata"]     = yourdata
        
        return data

    '''
    Analyse the summer data (smart water meter data - timeseries) of the logged user (household) for the specific year
    user:  logged user (See User object for details) - from this user a household can be obtained
    year:  year
    return: If no data exists for the specified period or dates then return None otherwise return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getsummerstats(user,"2012")    
    '''     
    def getsummerstats(self,loggeduser,year):
        maxyobj  = {"date":"","units":""}
        minyobj  = {"date":"","units":""}
        yourdata = {"max":"","min":"","sum":"","avg":"","occupant":""}
        data     = None
        household = loggeduser.households.all()[0] #get user household id         
        
        #hourly series
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_monthly = series.readseries(ts_monthly)

        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"

        start = year+"-06-01"
        end   = year+"-08-01"
                
        pdfysummer = pdf[start:end]
        months = pdfysummer.count()
        if months["units"]==3:
            youdtlist = pdfysummer.index.values
            youdtlist = [str(date.astype('M8[D]')) for date in youdtlist] #coverting numpy datetime64 to date string only
            list1     = pdfysummer.values
            
            #getting highest value
            maxyobj["date"] = youdtlist[np.argmax(list1)] #getting date from numpydatetime  
            maxyobj["units"]= np.amax(list1)
            
            #getting lowest value
            minyobj["date"] = youdtlist[np.argmin(list1)] #getting date from numpydatetime
            minyobj["units"]= np.amin(list1)                

            yourdata["max"]  = maxyobj
            yourdata["min"]  = minyobj                                                                          
            yourdata["sum"]  = np.sum(list1) # sum all values
            
            yourdata["avg"]  = yourdata["sum"]/list1.size #month average
            yourdata["occupant"] = yourdata["sum"]/household.num_of_occupants #month average

            data = series.getlistTojson(youdtlist,list1,"date","units")
            data.append({"yourdata":yourdata})
        
        return data

    '''
    Analyse the winter data (smart water meter data - timeseries) of the logged user (household) for the specific year
    user:  logged user (See User object for details) - from this user a household can be obtained
    year:  year
    return: If no data exists for the specified period or dates then return None other return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getwinterstats(user,"2009")    
    '''     
    def getwinterstats(self,loggeduser,year):
        maxyobj  = {"date":"","units":""}
        minyobj  = {"date":"","units":""}
        yourdata = {"max":"","min":"","sum":"","avg":"","occupant":""}
        data = None
        household = loggeduser.households.all()[0] #get user household id         
        
        #hourly series
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_monthly = series.readseries(ts_monthly)

        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"

        start = year+"-12-01"
        year  = str(int(year)+1)
        end   = year+"-02-01"
                
        pdfwinter = pdf[start:end]
        months = pdfwinter.count()
        if months["units"]==3:
            youdtlist = pdfwinter.index.values
            youdtlist = [str(date.astype('M8[D]')) for date in youdtlist] #coverting numpy datetime64 to date string only
            list1     = pdfwinter.values
            
            #getting highest value
            maxyobj["date"] = youdtlist[np.argmax(list1)] #getting date from numpydatetime  
            maxyobj["units"]= np.amax(list1)
            
            #getting lowest value
            minyobj["date"] = youdtlist[np.argmin(list1)] #getting date from numpydatetime
            minyobj["units"]= np.amin(list1)                

            yourdata["max"]  = maxyobj
            yourdata["min"]  = minyobj                                                                          
            yourdata["sum"]  = np.sum(list1) # sum all values
            
            yourdata["avg"]  = yourdata["sum"]/list1.size #month average
            yourdata["occupant"] = yourdata["sum"]/household.num_of_occupants #month average

            data = series.getlistTojson(youdtlist,list1,"date","units")
            data.append({"yourdata":yourdata})
        
        return data

    '''
    Analyse the logged user household seasonal data (time series) for the specific year and return the bill cost
    user:  logged user (See User object for details) - from this user a household can be obtained
    year:  year
    season: season names (summer, autumn, winter, spring)
    return: If no data exists for the specified period or dates then return None otherwise return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getseasonusage(user,"2012","autumn")    
    '''     
    def getseasonusage(self,loggeduser,year,season):
        '''
        prepare data structure
        '''
        stdate = "" #start date
        endate = "" #end date
        ts_monthly = None #for timeseries
        pdf        = None # for panda dataframe
        period = ""
        #dtlist = [] #for holding list of dates from panda dataframe
        list1  = [] #for holding list of data values from panda dataframe (tariff1)
        seasondata = {"household":0.0,"occupant":0.0} 
        series = iseries()
        data = {}
        #season period
        if season=="summer":
            stdate = year+"-06-01"
            midate = year+"-07-01"
            endate = year+"-08-01"   
            dtlist = [stdate,midate,endate]      
        elif season=="spring":
            stdate = year+"-03-01"
            midate = year+"-04-01"
            endate = year+"-05-01"
            dtlist = [stdate,midate,endate]
        elif season=="winter":
            stdate = year+"-12-01"
            midate = str(int(year)+1)+"-01-01"
            endate = str(int(year)+1)+"-02-01"
            dtlist = [stdate,midate,endate]  
        elif season=="autumn":
            stdate = year+"-09-01"
            midate = year+"-10-01"
            endate = year+"-11-01"  
            dtlist = [stdate,midate,endate]
        else:
            return None
                   
        #number of months to process data
        period = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1
        
        '''
        obtain timeseries for specified date range
        '''
        household = loggeduser.households.all()[0] #get user household id
        ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
        if ts_monthly:            
            '''
            prepare panda dataframe for processing timeseries data
            '''
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"                                   

            pdf = pdf[stdate:endate]
            if period != len(pdf.index):
                data = None
            elif pdf.empty:
                data = None
            else:                
                '''
                prepare data to be used in client (browser)
                Note: This code can be optimised if processed using panda dataframe. To do this ihousehold class tariff1 and tariff2 needs to be rewrite using panda dataframe
                '''
                dates  = pd.to_datetime(pdf.index.values)
                units  = pdf.values
                
                for x in range(0, period):
                    #dtlist.append(str(dates[x].strftime('%Y-%m-%d')))         
                    unit = float(units[x])
                    seasondata["household"] = seasondata["household"] + unit
                    list1.append(round(unit,2))
                                    
                seasondata["household"] = round(seasondata["household"],2)
                seasondata["occupant"]  = round(seasondata["household"]/household.num_of_occupants,2)
                                                       
                data["data"]        = series.getlistTojson(dtlist,list1,"date","units")
                data["yourdata"]    = seasondata
                
                '''
                add title to be displayed on top of graph
                
                #convert date from to easily read at client side (eg. December 2009
                stdate = iutility.convertdate(str(stdate),'%Y-%m-%d','%B-%Y')
                endate = iutility.convertdate(str(endate),'%Y-%m-%d','%B-%Y')
                data["title"]   = "UNITS COMPARISON FOR "+season.upper()+" ("+stdate+" TO "+endate+")"
                '''   
        else:
            data = None              
            
        return data
    
    '''
    Analyse the logged user household seasonal data (time series) for the specific year and return the bill cost
    user:  logged user (See User object for details) - from this user a household can be obtained
    year:  year
    season: season names (summer, autumn, winter, spring)
    return: If no data exists for the specified period or dates then return None otherwise return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getseasoncost(user,"2012","autumn")    
    '''     
    def getseasoncost(self,loggeduser,year,season):
        '''
        prepare data structure
        '''
        stdate = "" #start date
        endate = "" #end date
        ts_monthly = None #for timeseries
        pdf        = None # for panda dataframe
        period = ""
        dtlist = [] #for holding list of dates from panda dataframe
        list1  = [] #for holding list of data values from panda dataframe (tariff1)
        list2  = [] #for holding list of data values from panda dataframe (tariff2)
        tariff1data = {"sum":0.0,"avg":0.0,"high":0.0,"low":0.0}
        tariff2data = {"sum":0.0,"avg":0.0,"high":0.0,"low":0.0}
        comparechart=[{"Cost":"","Data":"Tariff1"},{"Cost":"","Data":"Tariff2"}] 
        series = iseries()
        data = {}
        #season period
        if season=="summer":
            stdate = year+"-06-01"
            endate = year+"-08-01"        
        elif season=="spring":
            stdate = year+"-03-01"
            endate = year+"-05-01"  
        elif season=="winter":
            stdate = year+"-12-01"
            endate = str(int(year)+1)+"-02-01"  
        elif season=="autumn":
            stdate = year+"-09-01"
            endate = year+"-11-01"  
        else:
            return None
                   
        #number of months to process data
        period = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1
        
        '''
        obtain timeseries for specified date range
        '''
        household = loggeduser.households.all()[0] #get user household id
        ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
        if ts_monthly:            
            '''
            prepare panda dataframe for processing timeseries data
            '''
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"                                   

            pdf = pdf[stdate:endate]
            if period != len(pdf.index):
                data = None
            elif pdf.empty:
                data = None
            else:                
                '''
                prepare data to be used in client (browser)
                Note: This code can be optimised if processed using panda dataframe. To do this ihousehold class tariff1 and tariff2 needs to be rewrite using panda dataframe
                '''
                dates  = pd.to_datetime(pdf.index.values)
                units  = pdf.values
                
                for x in range(0, period):
                    dtlist.append(str(dates[x].strftime('%Y-%m-%d')))         
                    tariff1 = self.tariff1(float(units[x]))
                    tariff1data["sum"] = tariff1data["sum"] + tariff1
                    list1.append(round(tariff1,2))
                                 
                    tariff2 = self.tariff2(float(units[x]))
                    tariff2data["sum"] = tariff2data["sum"] + tariff2
                    list2.append(round(tariff2,2))     
    
                tariff1data["sum"]      = round(tariff1data["sum"],2)
                tariff1data["avg"]      = round(tariff1data["sum"]/period,2)
                tariff1data["high"]     = {"date":iutility.convertdate(dtlist[list1.index(max(list1))],'%Y-%m-%d','%B-%Y'),"max":max(list1)} #max per nonth
                tariff1data["low"]      = {"date":iutility.convertdate(dtlist[list1.index(min(list1))],'%Y-%m-%d','%B-%Y'),"min":min(list1)} #min per nonth
                  
                tariff2data["sum"]      = round(tariff2data["sum"],2)                    
                tariff2data["avg"]      = round(tariff2data["sum"]/period,2)
                tariff2data["high"]     = {"date":iutility.convertdate(dtlist[list1.index(max(list1))],'%Y-%m-%d','%B-%Y'),"max":max(list1)} #max per nonth
                tariff2data["low"]      = {"date":iutility.convertdate(dtlist[list1.index(min(list1))],'%Y-%m-%d','%B-%Y'),"min":min(list1)} #min per nonth
                
                comparechart[0]["Cost"] = tariff1data["sum"]            
                comparechart[1]["Cost"] = tariff2data["sum"]    
                                       
                data["tariff1"]         = series.getlistTojson(dtlist,list1,"Date","Cost")
                data["tariff2"]         = series.getlistTojson(dtlist,list2,"Date","Cost")
                data["tariff1data"]     = tariff1data
                data["tariff2data"]     = tariff2data            
                data["comparechart"]    = comparechart
                '''
                add title to be displayed on top of graph
                '''
                #convert date from to easily read at client side (eg. December 2009
                stdate = iutility.convertdate(str(stdate),'%Y-%m-%d','%B-%Y')
                endate = iutility.convertdate(str(endate),'%Y-%m-%d','%B-%Y')
                data["title"]   = "TARIFF COMPARISON FOR "+season.upper()+" ("+stdate+" TO "+endate+")"
        else:
            data = None              
        
        return data
            
    '''
    Analyse the logged user household data (time series) and calculate bill
    user:  logged user (See User object for details) - from this user a household can be obtained
    months:number of recent months to calculate bill  
    return: If no data exists for the specified period or dates then return None otherwise return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getmonthlybill(user,3)    
    '''     
    def getmonthlybill(self,loggeduser,months):
        '''
        Declare data structure 
        '''
        dtlist = []
        list1  = []
        cost   = 0.0
        highest= 0.0
        lowest = 0.0
        billdata = {"sum":0.0,"avg":0.0,"high":"","low":"","occupant":""}
        data = {}     
        hhold  = ihousehold()
        series = iseries()
        
        #obtain time series
        household = loggeduser.households.all()[0]
        ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries        
        '''
        get the last 3 months time series to display by default
        '''
        length = len(ts_monthly)
        if length>=months:
            ts_monthly = ts_monthly[length-months:] #get the latest last 3 months
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            
            for x in range(0, months):
                dtlist.append(str(dates[x].date()))         
                cost = self.tariff1(float(units[x])) #subscribed to tariff1
                billdata["sum"] = billdata["sum"] + cost
                list1.append(round(cost,2))
            
            highest          = max(list1)
            lowest           = min(list1)
            billdata["sum"]  = round(billdata["sum"],2)
            billdata["avg"]  = round(billdata["sum"]/months,2)
            billdata["high"] = {"date":iutility.convertdate(dtlist[list1.index(highest)],'%Y-%m-%d','%B-%Y'),"max":highest} #max per nonth
            billdata["low"]  = {"date":iutility.convertdate(dtlist[list1.index(lowest)],'%Y-%m-%d','%B-%Y'),"min":lowest} #min per nonth
            billdata["occupant"]  = round(billdata["sum"]/household.num_of_occupants,2)
            data["data"]     = series.getlistTojson(dtlist,list1,"Date","Cost")
            data["billdata"] = billdata        
            data["title"]    = "LAST "+ str(months) +" MONTHS BILL"
            
            '''
            price break lines
            '''
            start = dtlist[0]
            end   = dtlist[months-1]
            data["price_break"] = [
                           { "Price Break" : "Highest", "Cost" : highest, "Date" : start }, 
                           { "Price Break" : "Highest", "Cost" : highest, "Date" : end },
                           { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : start }, 
                           { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : end },
                           { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : start }, 
                           { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : end }
                       ];                    
        else:
            data = None 
            
        #sum  = series.getCost(series.getSum(tseries_month))
        #high = json.dumps(series.getHighestCost(tseries_month)) #still need to write function to get cost
        #low  = json.dumps(series.getLowestCost(tseries_month))  #still need to write function to get cose
        #avg  = series.getCost(series.getAvg(tseries_month,len(tseries_month)))
        #tsmonth = json.dumps(series.getseriesTojsoncost(tseries_month,"cost"))        
        return data
       
    '''
    Analyse the logged user household data (time series) and calculate usage
    user:  logged user (See User object for details) - from this user a household can be obtained
    months:number of recent months to analyse units consumed  
    return: If no data exists for the specified period or dates then return None otherwise return statistics    
        >>> h = ihousehold()
        >>> user = request.user           
        >>> h.getmonthlyusage(user,3)    
    '''   
    def getmonthlyusage(self,loggeduser,months):
        '''
        Declare data structure 
        '''
        dtlist = []
        list1  = []
        cost   = 0.0
        highest= 0.0
        lowest = 0.0
        billdata = {"sum":0.0,"avg":0.0,"high":"","low":"","occupant":0.0,"household":0.0}
        data = {}     
        hhold  = ihousehold()
        series = iseries()
        
        #obtain time series
        household  = loggeduser.households.all()[0]
        ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries        
        '''
        get the last 3 months time series to display by default
        '''
        length = len(ts_monthly)
        if length>=months:
            ts_monthly = ts_monthly[length-months:] #get the latest last 3 months
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            
            for x in range(0, months):
                dtlist.append(str(dates[x].date()))         
                cost = float(units[x]) #subscribed to tariff1
                billdata["sum"] = billdata["sum"] + cost
                list1.append(round(cost,2))
                
            highest          = max(list1)
            lowest           = min(list1)
            billdata["sum"]  = round(billdata["sum"],2)
            billdata["household"] = round(billdata["sum"],2)
            billdata["avg"]  = round(billdata["sum"]/months,2)
            billdata["high"] = {"date":iutility.convertdate(dtlist[list1.index(highest)],'%Y-%m-%d','%B-%Y'),"max":highest} #max per nonth
            billdata["low"]  = {"date":iutility.convertdate(dtlist[list1.index(lowest)],'%Y-%m-%d','%B-%Y'),"min":lowest} #min per nonth
            billdata["occupant"]  = round(billdata["sum"]/household.num_of_occupants,2)
            
            data["data"]     = series.getlistTojson(dtlist,list1,"Date","Cost")
            data["yourdata"] = billdata        
            data["title"]    = "LAST "+ str(months) +" MONTHS BILL"
            
            '''
            price break lines
            '''
            start = dtlist[0]
            end   = dtlist[months-1]
            data["price_break"] = [
                           { "Price Break" : "Highest", "Cost" : highest, "Date" : start }, 
                           { "Price Break" : "Highest", "Cost" : highest, "Date" : end },
                           { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : start }, 
                           { "Price Break" : "Average", "Cost"  :billdata["avg"], "Date"  : end },
                           { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : start }, 
                           { "Price Break" : "Lowest", "Cost"  : lowest, "Date"  : end }
                       ];       
        else:
            data = None 
            
        #sum  = series.getCost(series.getSum(tseries_month))
        #high = json.dumps(series.getHighestCost(tseries_month)) #still need to write function to get cost
        #low  = json.dumps(series.getLowestCost(tseries_month))  #still need to write function to get cose
        #avg  = series.getCost(series.getAvg(tseries_month,len(tseries_month)))
        #tsmonth = json.dumps(series.getseriesTojsoncost(tseries_month,"cost"))        
        return data
                                      
    def getUsage(self,loggeduser):
        '''
        Calculating household monthly cost and other statistics
        '''
        dic12 = {"period":"","sum_units":"","avg_units":"","unit_person":""}
        household  = loggeduser.households.all()[0]
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household) 
        timeseries_monthly = series.readseries(ts_monthly)
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
        pdf   =  pd.DataFrame(list(units),index=list(dates),columns=["units"]) #create pandas Series (time series using two different list for timeseries data analysis
        #last 12 months
        pdf12 = pdf.ix[-12:] #get last 12 months
        dic12["period"] = "12 Months"
        dic12["sum_units"] = round(np.sum(pdf12.values),2)
        dic12["avg_units"] = round(dic12["sum_units"]/12,2)
        dic12["unit_person"]= round(dic12["sum_units"]/household.num_of_occupants,2)
        #last 6 months
        dic6  = dic12.copy()
        pdf6  = pdf.ix[-6:] #get last 6 months
        dic6["period"] = "6 Months"
        dic6["sum_units"] = round(np.sum(pdf6.values),2)
        dic6["avg_units"] = round(dic6["sum_units"]/6,2)
        dic6["unit_person"] = round(dic6["sum_units"]/household.num_of_occupants,2)
        #last 4 months
        dic4  = dic12.copy()
        pdf4  = pdf.ix[-3:] #get last 6 months
        dic4["period"] = "3 Months"
        dic4["sum_units"] = round(np.sum(pdf4.values),2)
        dic4["avg_units"] = round(dic4["sum_units"]/3,2)
        dic4["unit_person"] = round(dic4["sum_units"]/household.num_of_occupants,2)
        #last 1 month
        pdf1  = pdf.ix[-1:] #get last 1 month
        dic1  = dic12.copy()
        dic1["period"]    = "1 Month"
        dic1["sum_units"] = round(np.sum(pdf1.values),2)
        dic1["avg_units"] = round(dic1["sum_units"],2)
        dic1["unit_person"] = round(dic1["sum_units"]/household.num_of_occupants,2)
        #combine all data
        data = {"year":dic12,"half":dic6,"quarter":dic4,"month":dic1}
        return data

        
    #logged user: It is the currently logged user
    def gethousehold(self,loggeduser,id=None):
        try:
            if id is not None:
                household = Household.objects.filter(pk=id)
            else:
                household =  loggeduser.households.filter(user__pk=loggeduser.pk) #user is a one-to-on relation in household table and can be queried using reverse relationship
            serialize = iserialize()
            return serialize.modelToJSON(household,self.col)
        except: #if pass wrong household id
            return -1 #indcates other issues or errors, it needs to be redirected to universal error
    
    #logged user: It is the currently logged user
    #values is a dictionary of values. It must be the combination of {database column:database value}
    def updatehousehold(self,loggeduser,values):
        try:
            del values['csrfmiddlewaretoken'] #make sure to get rid of any csrfmiddlewaretoken before comitting saving to db 
        except:
            pass
                
        try:
            loggeduser.households.filter(user__pk=loggeduser.pk).update(**values)
            return True  #household details save successfully
        except:
            return -1 #indcates other issues or errors, it needs to be redirected to universal error            
            