'''
Created on 01 Apr 2014

@author: adeel
'''
from iwidget.models import *
from unexe.models import userDMAstats, Forecast, DMAstats
from Idma import idma
from Iseries import iseries
from Iutility import iutility
from Ihousehold import ihousehold
from py4j.java_gateway import JavaGateway, GatewayClient
import json, datetime
import pandas as pd
import itertools as IT
import numpy as np
from unexe.classes.Ifile import ifile

class iusecase():
    def __init__(self,User):
        self.User = User

    '''
    Use case 3.3 method to perform initial computation that will show appear as default chart
    '''
    def usecase3_3(self):
        '''
        Calculating household monthly cost and other statistics
        '''
        hhold  = ihousehold()
        hholdstats = hhold.getUsage(self.User)
        #print hholdstats
        household = self.User.households.all()[0]
        dma = DMA.objects.get(pk=11) #chosing other DMA for comparison, we will change this when we will get the different demographic database
        household_dma = dma.households.all()
        d = idma()
        series = iseries()
        obj   = {}
        list1 = []
        areadata = {"year":"","half":"","quarter":"","month":""}
        yourdata = {"year":"","half":"","quarter":"","month":""}
        #getting consumer with same socio-demographic status for the average unit/bill
        for x in range(0, 4):
            if x==0:
                period = 12
                cal    = "year"
            elif x==1:
                period = 6
                cal    = "half"
            elif x==2:
                period = 3
                cal    = "quarter"                            
            elif x==3:
                period = 1
                cal    = "month"
                                
            dic = d.getStats(household_dma,period)
            areadata[cal] = dic
            obj["Units"] = dic["avg_units"]
            obj["Cost"]  = round(hhold.tariff1(dic["avg_units"]),2)
            #obj["Cost"]  = str(series.getCost(dic["avg_units"]))
            obj["Period"]= str(period)+" Month"
            obj["Data"]  = "Area"
            list1.append(obj)
            obj = {}
            dic = {}
            dic = hholdstats[cal]
            yourdata[cal] = dic
            #print dic
            obj["Units"] = str(dic["sum_units"])
            obj["Cost"]  = round(hhold.tariff1(dic["sum_units"]),2)
            #obj["Cost"]  = str(series.getCost(dic["sum_units"]))
            obj["Period"]= str(period)+" Month"
            obj["Data"]  = "You"
            dic = {}
            list1.append(obj)          
            obj = {}

        data = {}
        data["chart"]    = list1
        data["areadata"] = areadata
        data["yourdata"] = yourdata

        return data
    
    '''
    This method contains the default implementation of the use case 5.2. Use case 5.2 aim is to show the Household consumer water bill calculated using different tariffs or 
    pricing scheme. consumer latest 2 months data (Minimum comparison units) will be used to calcute bills using different pricing schema and display in the form of charts,
    values in tables etc. If there is no latest data then a message by default will appear that "statistics will be displayed after 2 months of data/bill"  
    '''
    def usecase5_2(self):
        '''
        Declare data
        '''
        dtlist = []
        list1  = []
        tariff1data = {"sum":0.0,"avg":0.0,"high":0.0,"low":0.0}
        tariff2data = {"sum":0.0,"avg":0.0,"high":0.0,"low":0.0}
        comparechart=[{"Cost":"","Data":"Tariff1"},{"Cost":"","Data":"Tariff2"}]
        stdate = ""
        endate = ""
        data = {}
                
        household = self.User.households.all()[0]
        hhold  = ihousehold()
        series = iseries()
        ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries

        if len(ts_monthly)>=2:  #at least 2 months data
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"]) #create pandas Series (time series using two different list for timeseries data analysis
            pdf.index.name = "dates"
            
            #list of dates (chosen the latest two months of the time series)
            stdate = str(dates[len(dates)-2].date())
            endate = str(dates[len(dates)-1].date())
            
            dtlist.append(stdate)
            dtlist.append(endate)
            
            list1.append(round(hhold.tariff1(units[len(units)-2]),2))
            list1.append(round(hhold.tariff1(units[len(units)-1]),2))
            data["tariff1"] = series.getlistTojson(dtlist,list1,"Date","Cost")
            
            tariff1data["sum"]  = list1[0] + list1[1]    # sum over month for this tariff
            tariff1data["avg"]  = round(tariff1data["sum"]/len(list1),2) #average per nonth
            tariff1data["high"] = {"date":iutility.convertdate(dtlist[list1.index(max(list1))],'%Y-%m-%d','%B-%Y'),"max":max(list1)} #max per nonth
            tariff1data["low"]  = {"date":iutility.convertdate(dtlist[list1.index(min(list1))],'%Y-%m-%d','%B-%Y'),"min":min(list1)} #min per nonth
            data["tariff1data"] = tariff1data 
            comparechart[0]["Cost"] = tariff1data["sum"]
            
            
            list1 = []    
            list1.append(round(hhold.tariff2(units[len(units)-2]),2))
            list1.append(round(hhold.tariff2(units[len(units)-1]),2))
            data["tariff2"] = series.getlistTojson(dtlist,list1,"Date","Cost")
            
            tariff2data["sum"]  = list1[0] + list1[1]    # sum over month for this tariff
            tariff2data["avg"]  = round(tariff2data["sum"]/len(list1),2) #average per nonth
            tariff2data["high"] = {"date":iutility.convertdate(dtlist[list1.index(max(list1))],'%Y-%m-%d','%B-%Y'),"max":max(list1)} #max per nonth
            tariff2data["low"]  = {"date":iutility.convertdate(dtlist[list1.index(min(list1))],'%Y-%m-%d','%B-%Y'),"min":min(list1)} #min per nonth
            data["tariff2data"] = tariff2data
            comparechart[1]["Cost"] = tariff2data["sum"]
            data["comparechart"]= comparechart 

            '''
            add title to be displayed on top of graph
            '''
            #convert date from to easily read at client side (eg. December 2009
            stdate = iutility.convertdate(str(stdate),'%Y-%m-%d','%B-%Y')
            endate = iutility.convertdate(str(endate),'%Y-%m-%d','%B-%Y')
            data["title"]   = "TARIFF COMPARISON FROM "+stdate+" TO "+endate
        else:
            data = None
        
        #print data
        return data
        '''
        qt = 3
        qtmonth = []
        #hourly series
        ts_hourly = series.gethourlyseries(household)
        timeseries_hourly = series.readseries(ts_hourly)
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_hourly) #much better for longer data, returning tuples
        pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"]) #create pandas Series (time series using two different list for timeseries data analysis
        #ulist = units.split(",")        
        #print ulist
        #extract the last quarter (4 months) from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole month
        #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value
        today = iutility.getstrTodate("2010-02-01","%Y-%m-%d")
        today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d")
        
        dtlist = []
        list1 = []
        list2 = []
        for x in range(qt,0,-1):
            qtmonth.append(iutility.subtract_year_month(today,month=x))
            firstday = iutility.subtract_year_month(today,month=x)
            lastday  = iutility.last_day_month(firstday)
            pdfmonth = pdf[firstday:lastday]
            pdfday   = pdfmonth.between_time('07:00','17:00')
            pdfnight = pdfmonth.between_time('18:00','06:00')
            dtlist.append(str(firstday))
            list1.append(np.sum(pdfday.values))
            list2.append(np.sum(pdfnight.values))
        
        #print series.getlistTojson(dtlist,list1,"date","units")
        #print dtlist
        #print list1
        #print list2
        #start = iutility.subtract_year_month(today,month=4)
        #finish= iutility.subtract_year_month(today,month=1)
        #start = str(start.year)+"-"+str(start.month)
        #finish= str(finish.year)+"-"+str(finish.month)
        #start  = qtmonth[3] 
        #end = qtmonth[0]
        #[{'date': '2010-02-01', 'cost': 10.275334396755488}, {'date': '2010-03-01', 'cost': 7.936416401490733}, {'date': '2010-04-01', 'cost': 10.233750913048016}]
           
                
        #ptsQt = pdf[str(qtmonth[3].year)+"-"+str(qtmonth[3].month):str(qtmonth[0].year)+"-"+str(qtmonth[0].month)] #timseries for the last quarter
        #dr = pd.DateRange(start,iutility.last_day_month(start), offset=pd.datetools.Hour())        
        #print dr
        #hr = dr.map(lambda x: x.hour)
        #print qtmonth[3]
        #print iutility.last_day_month(qtmonth[3])
        #t = pts[qtmonth[3]:iutility.last_day_month(qtmonth[3])]
        #print t
        #t = temp.between_time('00:00','01:00')
        #print t
        #print np.sum(t.values)
        #print qtmonth[2]
        #print iutility.last_day_month(qtmonth[2])        
        #t = pts["2009-04-01":"2009-04-30"]
        #print np.sum(t.values)
        #Qtday = ptsQt.between_time('07:00','17:00') #day units for the first month of the quarter
        #Qteve = ptsQt.between_time('18:00','06:00') #day units for the first month of the quarter
        #print np.sum(Qtday.values)
        #print np.sum(Qteve.values)
        #print ptsQt
        #print pts
        '''

    
    '''
    Private method that saves dmastats to database
    household: This is the Household models objects (queryset)
    dma: This is the logged user dma
    period: number of months to calculate statistics
    
    '''
    def __savedbdmastats(self,household,dma,period):
        d       = idma()
        stats   = d.getStats(household,period) #get stats for all user in DMA that has at least 12 months time series data
        dmastats= DMAstats.objects.create(statsperiod=period,sumhouseholds=stats["sum_households"],sumoccupants=stats["sum_occupants"],sumunits=stats["sum_units"],
                                           maxoccupants=stats["max_occupants"],avgoccupants=stats["avg_occupants"],minoccupants=stats["min_occupants"],
                                           maxunits=stats["max_units"],avgunits=stats["avg_units"],minunits=stats["min_units"],dma=dma)        
        return
    
    '''
    Private method that saves userdmastats to database
    household: This is the Household models objects (queryset)
    dma: This is the logged user dma
    period: number of months to calculate statistics
    options: This is the filtered option: (1=num of occupants, 2=property type, 3=number of occupants+property type)
    
    '''
    def __savedbuserdmastats(self,household,period,option):
        d       = idma()
        stats    = d.gethouseholdstats(household,period) #get stats for all user in DMA that has at least 12 months time series data
        dmastats = userDMAstats.objects.create(statsperiod=period,sumhouseholds=stats["sum_households"],sumoccupants=stats["sum_occupants"],sumunits=stats["sum_units"],
                                maxunits=stats["max_units"],avgunits=stats["avg_units"],minunits=stats["min_units"],household=self.User.households.all()[0],options=option) 
        return
        
    def usecase3_2(self):
        data = {}
        household = self.User.households.all()[0]
        dma = household.dma
        series = iseries()
        d        = idma()
        '''
        start of all user statistics in DMA
        '''        
        #dict = {"sum_households":"","avg_occupants":""}
        #dict["sum_households"] = Household.objects.filter(dma__pk=dma.pk).count() #total household
        #dict["avg_occupants"]  = Household.objects.filter(dma__pk=dma.pk).aggregate(Sum("num_of_occupants"))
        #dict["avg_occupants"]  = dict["avg_occupants"]["num_of_occupants__sum"]/dict["sum_households"]
        #print dict
        
        household_dma = dma.households.all() #get all households in logged user DMA
        '''#start
        dmastats = DMAstats.objects.filter(dma__pk=dma.pk)            
        
        #dmasummary = d.getStats(household_dma,0)
        #print dict
        if not dmastats: #if no statistics ever computed before for this DMA
            self.__savedbdmastats(household_dma,dma,12)
            self.__savedbdmastats(household_dma,dma,6)
            self.__savedbdmastats(household_dma,dma,4)
            self.__savedbdmastats(household_dma,dma,1)           
        else: #if stats exists then check it is updated in the last 24 hours
            for st in dmastats:
                if datetime.date.today() > st.statsdate:
                    stats = d.getStats(household_dma,st.statsperiod)
                    st.statsdate = datetime.date.today()
                    st.sumhouseholds=stats["sum_households"]
                    st.sumoccupants=stats["sum_occupants"]
                    st.sumunits=stats["sum_units"]
                    st.maxoccupants=stats["max_occupants"]
                    st.avgoccupants=stats["avg_occupants"]
                    st.minoccupants=stats["min_occupants"]
                    st.maxunits=stats["max_units"]
                    st.avgunits=stats["avg_units"]
                    st.minunits=stats["min_units"]
                    st.dma=dma
                    st.save();
        '''#end
        '''
        End of all user statistics in DMA
        '''

        '''
        Start of DMA user statistics based on filter information
        1) Based on number of occupants 
        '''
        '''#start                    
        dmastats  = userDMAstats.objects.filter(household=household)
        #household_dma = dma.households.exclude(user=self.User) #exclude logged user from DMA
                 
        if not dmastats:
            household_dma = dma.households.exclude(user=self.User) #exclude logged user from DMA
            household_dma = household_dma.filter(num_of_occupants=household.num_of_occupants) #get households with the same of household as like logged user            
            self.__savedbuserdmastats(household_dma,12,1)
            self.__savedbuserdmastats(household_dma,6,1)
            self.__savedbuserdmastats(household_dma,4,1)
            self.__savedbuserdmastats(household_dma,1,1)

            household_dma = dma.households.exclude(user=self.User) #exclude logged user from DMA
            household_dma = household_dma.filter(property_type=household.property_type) #get households with the same of household as like logged user            
            self.__savedbuserdmastats(household_dma,12,2)
            self.__savedbuserdmastats(household_dma,6,2)
            self.__savedbuserdmastats(household_dma,4,2)
            self.__savedbuserdmastats(household_dma,1,2)

            household_dma = dma.households.exclude(user=self.User) #exclude logged user from DMA
            household_dma = household_dma.filter(num_of_occupants=household.num_of_occupants,property_type=household.property_type) #get households with the same of household as like logged user            
            self.__savedbuserdmastats(household_dma,12,3)
            self.__savedbuserdmastats(household_dma,6,3)
            self.__savedbuserdmastats(household_dma,4,3)
            self.__savedbuserdmastats(household_dma,1,3)
        else: #if stats exists then check it is updated in the last 24 hours
            for st in dmastats:
                if datetime.date.today() > st.statsdate:
                    stats = d.gethouseholdstats(household_dma,st.statsperiod)
                    st.statsdate = datetime.date.today()
                    st.sumhouseholds=stats["sum_households"]
                    st.sumoccupants=stats["sum_occupants"]
                    st.sumunits=stats["sum_units"]
                    st.maxunits=stats["max_units"]
                    st.avgunits=stats["avg_units"]
                    st.minunits=stats["min_units"]
                    st.household=household
                    st.save();
        '''#end
        hhold  = ihousehold()
        hholdstats = hhold.getUsage(self.User)
        #print hholdstats
        #household = self.User.households.all()[0]
        #dma = DMA.objects.get(pk=10) #chosing other DMA for comparison, we will change this when we will get the different demographic database
        #household_dma = dma.households.all()
        #d = idma()
        #series = iseries()
        obj   = {}
        list1 = []
        areadata = {"year":"","half":"","quarter":"","month":""}
        yourdata = {"year":"","half":"","quarter":"","month":""}
        #getting consumer with same socio-demographic status for the average unit/bill
        for x in range(0, 4):
            if x==0:
                period = 12
                cal    = "year"
            elif x==1:
                period = 6
                cal    = "half"
            elif x==2:
                period = 3
                cal    = "quarter"                            
            elif x==3:
                period = 1
                cal    = "month"
                                
            dic = d.getStats(household_dma,period)
            areadata[cal] = dic
            obj["Units"] = dic["avg_units"]
            obj["Cost"]  = round(hhold.tariff1(dic["avg_units"]),2)
            #obj["Cost"]  = str(series.getCost(dic["avg_units"]))
            obj["Period"]= str(period)+" Month"
            obj["Data"]  = "Area"
            list1.append(obj)
            obj = {}
            dic = {}
            dic = hholdstats[cal]
            yourdata[cal] = dic
            #print dic
            obj["Units"] = str(dic["sum_units"])
            obj["Cost"]  = round(hhold.tariff1(dic["sum_units"]),2)
            #obj["Cost"]  = str(series.getCost(dic["sum_units"]))
            obj["Period"]= str(period)+" Month"
            obj["Data"]  = "You"
            dic = {}
            list1.append(obj)          
            obj = {}

        data = {}
        data["chart"]    = list1
        data["areadata"] = areadata
        data["yourdata"] = yourdata

        return data
    
    def usecase5_3(self,User,tsmonthly,tsdaily):
        series = iseries()
        hhold  = ihousehold()   
        data   = hhold.getmonthlybill(self.User,3) 

        try:
            forecast = Forecast.objects.get(user=User) #get the current user forecast model object
            if not forecast.dailyfile:
                if  len(tsdaily)>0:
                    gateway = JavaGateway() #connect to JVM
                    entry = gateway.entry_point
                    ts = entry.getTimeSeries(str(User.id)) #get JAVA timeseries Object for this user                
                    path = ts.getdayArff()
                    '''
                    The method runs in a separate JAVA thread so it will not block the application, however if the thread runs for very long time  
                    for file writing and Iforecast class request the forecasting athen code needs to be block until the thread completes writing the file. 
                    '''                                
                    ts.writedayArff(json.dumps(series.getseriesTojson(tsdaily,"cost")),path)
                    '''
                    End of thread
                    '''                
                    #write path to db
                    forecast.dailyfile = path
                    forecast.dailydate = series.getfinaldate(tsdaily)
                    forecast.save()  
            else:
                #if newer data then append that day to file
                seriesdate = series.getfinaldate(tsdaily)
                dbdate     = forecast.dailydate
                if seriesdate > dbdate:
                    diff   = seriesdate - dbdate
                    diff = diff.days
                    list = tsdaily[len(tsdaily)-diff:]
                    line = ""
                    for i in list:
                        line = line + str(i[0].date())+","+str(i[1])+"\n"
                     
                    f = ifile(forecast.dailyfile,"a")
                    f.write(line)
                    f.close()
                    forecast.dailydate = seriesdate
                    forecast.save()
                    
            if not forecast.yearfile:
                if len(tsmonthly)>0:
                    gateway = JavaGateway() #connect to JVM
                    entry = gateway.entry_point
                    ts = entry.getTimeSeries(str(User.id)) #get JAVA timeseries Object for this user
                    path = ts.getyearlyArff()
                    '''
                    The method runs in a separate JAVA thread so it will not block the application, however if the thread runs for very long time  
                    for file writing and Iforecast class request the forecasting athen code needs to be block until the thread completes writing the file. 
                    '''                                
                    ts.writeyearlyArff(json.dumps(series.getseriesTojson(tsmonthly,"cost")),path)
                    '''
                    End of thread
                    '''                                
                    #write path to db
                    forecast.yearfile = path
                    forecast.yeardate = series.getfinaldate(tsmonthly)
                    forecast.save()
            else:
                #if newer data then append that month to file
                seriesdate = series.getfinaldate(tsmonthly)
                dbdate     = forecast.yeardate 
                if seriesdate > dbdate:
                    diff = iutility.diffmonth(seriesdate,dbdate) #get the mumber of months to append series to file
                    list = tsmonthly[len(tsmonthly)-diff:]
                    line = ""
                    for i in list:
                        #print (tseries[len(tseries)-1:][0][0]).date()
                        line = line + str(i[0].date())+","+str(i[1])+"\n"
                     
                    f = ifile(forecast.yearfile,"a")
                    f.write(line)
                    f.close()
                    forecast.yeardate = seriesdate
                    forecast.save()
                    
        except: #exception result if no record exists
            gateway = JavaGateway() #connect to JVM
            entry = gateway.entry_point            
            ts = entry.getTimeSeries(str(User.id)) #get JAVA timeseries Object for this user
            forecast = Forecast.objects.create(user=User)
            #ts.safeThread();
            #entry.shutGateway()
            if len(tsmonthly)>0:
                path = ts.getyearlyArff()
                '''
                The method runs in a separate JAVA thread so it will not block the application, however if the thread runs for very long time  
                for file writing and Iforecast class request the forecasting athen code needs to be block until the thread completes writing the file. 
                '''                
                ts.writeyearlyArff(json.dumps(series.getseriesTojson(tsmonthly,"cost")),path)
                '''
                End of thread
                '''                
                #write path to db
                forecast.yearfile = path
                forecast.yeardate = series.getfinaldate(tsmonthly)
                forecast.save()                
            
            if len(tsdaily)>0:
                path = ts.getdayArff()
                '''
                The method runs in a separate JAVA thread so it will not block the application, however if the thread runs for very long time  
                for file writing and Iforecast class request the forecasting athen code needs to be block until the thread completes writing the file. 
                '''                                
                ts.writedayArff(json.dumps(series.getseriesTojson(tsdaily,"cost")),path)
                '''
                End of thread
                '''                                
                #write path to db
                forecast.dailyfile = path
                forecast.dailydate = series.getfinaldate(tsdaily)
                forecast.save()        
        return data