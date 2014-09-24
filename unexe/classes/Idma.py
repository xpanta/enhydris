'''
Created on 17 Apr 2014

@author: adeel
'''
from Iseries import iseries
from Iutility import iutility
import Ihousehold
import datetime
import pandas as pd
import numpy as np
import itertools as IT
import math
'''
This is the class that deals with DMA. Here Household in the DMA is analyse to get useful statistics.
Due to large number of household in the DMA, most of the methods computes the DMA statistics at regular interval
and save the statistics in the Database. This can then me used by the individual household to compare their usage
against household in the DMA
'''
class idma():
    
    '''
    analyse the household's summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> d.getmonthlyusagefficient(household_dma,6)    
    '''
    def getmonthlyusagefficient(self,dma,months):
        start = ""
        mid   = ""
        end   = ""
        area  = {}
        areadata = {"sum":"","household":"","occupant":""}
        sumonth  = {}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0
        occupants = 0
        list1  = []
        dtlist = []
        first  = True
        
        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            length     = len(ts_monthly)
            if not length>=months:  #Total three months in the winter
                continue

            ts_monthly = ts_monthly[length-months:] #get the latest last 3 months
            #get dates and values in a separate list
            dates, mylist = IT.izip(*ts_monthly) #much better for longer
            units  = [float(round(n, 2)) for n in mylist] 
            if not dtlist:
                for x in range(0,months): 
                    dtlist.append(str(dates[x].date()))
                    list1.append(0.0)

            #sumhhold = sumhhold + 1 #number of household
            #sumoccup = sumoccup + household.num_of_occupants #number of occupants
            for x in range(0,months):
                if math.isnan(units[x]):
                    continue
                if first:
                    occupants = household.num_of_occupants
                    list1[x]  = units[x]
                    first     = False
                else:
                    if list1[x] == 0.0:
                        list1[x] = units[x]
                    else:
                        if units[x] < list1[x]:
                            list1[x] = units[x]                        
     
        
        '''
        If exists households
        '''
        if first==False:                                             
            areadata["sum"]       = sum(list1,2)
            areadata["household"] = round(areadata["sum"],2) #each month represents 1 household and in every season there are months in total
            areadata["occupant"]  = round(areadata["household"]/occupants,2) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
            area["areadata"]      = areadata
            area["data"]          = series.getlistTojson(dtlist,list1,"Date","Cost")
        else:
            area                  = None
        
        
        return area
        
    '''
    analyse the household's summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> getseasonusageefficient(household_dma,"2010","autumn")    
    '''
    def getseasonusagefficient(self,dma,year,season):
        start = ""
        mid   = ""
        end   = ""
        area  = {}
        areadata = {"sum":"","household":"","occupant":""}
        sumonth  = {}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0
        occupants     = 0
        first         = True
        mylist        = [0.0,0.0,0.0]
        
        if season=="winter":
            start = year+"-12-01"
            year  = str(int(year)+1)
            mid   = year+"-01-01"
            end   = year+"-02-01"
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="summer":
            start = year+"-06-01"
            mid   = year+"-07-01"
            end   = year+"-08-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="autumn":
            start = year+"-09-01"
            mid   = year+"-10-01"
            end   = year+"-11-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="spring":
            start = year+"-03-01"
            mid   = year+"-04-01"
            end   = year+"-05-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0} 

        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if not len(ts_monthly)>=3:  #Total three months in the winter
                continue

            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"
            pdfsummer = pdf[start:end]            
            months    = pdfsummer.count()
            if months["units"]==3: #if there are three winter months
                list1 = pdfsummer.values            
                if first:
                    occupants = household.num_of_occupants
                    sumonth[start] = list1[0]                        
                    sumonth[mid]   = list1[1]                        
                    sumonth[end]   = list1[2]
                    first              = False
                else:
                    if sumonth[start]==0.0:
                        sumonth[start] = list1[0]
                    else:
                        if list1[0] < sumonth[start]:
                            sumonth[start] = list1[0]
                            
                    if sumonth[mid]==0.0:
                        sumonth[mid] = list1[1]
                    else:
                        if list1[1] < sumonth[mid]:
                            sumonth[mid] = list1[1]

                    if sumonth[end]==0.0:
                        sumonth[end] = list1[2]
                    else:
                        if list1[2] < sumonth[end]:
                            sumonth[end] = list1[2]
                                                                                    
                           
        if first==False: #household are processed 
            list1[0] = sumonth[start]
            list1[1] = sumonth[mid]
            list1[2] = sumonth[end]
            
            mylist                = [float(round(n, 2)) for n in list1]
            areadata["sum"]       = sum(mylist)
            areadata["household"] = round(areadata["sum"],2) #each month represents 1 household and in every season there are months in total 
            areadata["occupant"]  = round(areadata["household"]/occupants,2) # this is the time
            
            area["areadata"]      = areadata
            dtlist                = [start,mid,end]
            area["data"]          = series.getlistTojson(dtlist,mylist,"date","units")
        else:
            area = None

        return area
        
    '''
    analyse the household's summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> getseasonusage(household_dma,"2010","autumn")    
    '''
    def getseasonusage(self,dma,year,season):
        start = ""
        mid   = ""
        end   = ""
        area  = {}
        areadata = {"sum":"","household":"","occupant":""}
        sumonth  = {}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0

        if season=="winter":
            start = year+"-12-01"
            year  = str(int(year)+1)
            mid   = year+"-01-01"
            end   = year+"-02-01"
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="summer":
            start = year+"-06-01"
            mid   = year+"-07-01"
            end   = year+"-08-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="autumn":
            start = year+"-09-01"
            mid   = year+"-10-01"
            end   = year+"-11-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0}
        elif season=="spring":
            start = year+"-03-01"
            mid   = year+"-04-01"
            end   = year+"-05-01"                
            sumonth = {start:0.0,mid:0.0,end:0.0}            
            
        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if not len(ts_monthly)>=3:  #Total three months in the winter
                continue

            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"
             
            pdfsummer = pdf[start:end]
            months    = pdfsummer.count()
            if months["units"]==3: #if there are three winter months
                sumhhold = sumhhold + 1 #number of household
                sumoccup = sumoccup + household.num_of_occupants #number of occupants 
                #youdtlist = pdfsummer.index.values
                #youdtlist = [str(date.astype('M8[D]')) for date in youdtlist]
                list1          = pdfsummer.values
                sumonth[start] = sumonth[start] + list1[0]
                sumonth[mid]   = sumonth[mid]   + list1[1]
                sumonth[end]   = sumonth[end]   + list1[2]
                unitshhold = unitshhold + np.sum(list1) #sum of all units for every household

        if sumhhold>0:     
            list1[0] = round(sumonth[start]/sumhhold,2)
            list1[1] = round(sumonth[mid]/sumhhold,2)
            list1[2] = round(sumonth[end]/sumhhold,2)    
            dtlist   = [start,mid,end]
            
            areadata["sum"]       = round(unitshhold,2)
            
            areadata["household"] = round(unitshhold/sumhhold,2) #units consume per household
            areadata["occupant"]  = round(areadata["household"]/(float(sumoccup)/float(sumhhold)),2) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
            area["areadata"]      = areadata
            area["data"]          = series.getlistTojson(dtlist,list1,"date","units")
        else:
            area                  = None
        
        return area
   
    '''
    analyse the household's summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> d.getmonthlyusage(household_dma,"2010","autumn")    
    '''
    def getmonthlyusage(self,dma,months):
        start = ""
        mid   = ""
        end   = ""
        area  = {}
        areadata = {"sum":"","household":"","occupant":""}
        sumonth  = {}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0
        list1  = []
        dtlist = []
        
        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            length = len(ts_monthly)
            if not length>=months:  #Total three months in the winter
                continue

            ts_monthly = ts_monthly[length-months:] #get the latest last 3 months
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer
            
            if not dtlist:
                for x in range(0,months): 
                    dtlist.append(str(dates[x].date()))
                    list1.append(0.0)

            sumhhold = sumhhold + 1 #number of household
            sumoccup = sumoccup + household.num_of_occupants #number of occupants
            for x in range(0,months):
                if math.isnan(units[x]):
                    continue
                list1[x] = list1[x] + units[x]
                  
        '''
        If exists households
        '''
        if sumhhold>0: 
            unitshhold = np.sum(list1) #sum of all units for every household
            for x in range(0,months):
                list1[x] = round(list1[x]/sumhhold,2)
                                            
            areadata["sum"]       = round(unitshhold,2)
            areadata["household"] = round(unitshhold/sumhhold,2) #units consume per household
            areadata["occupant"]  = round(areadata["household"]/(float(sumoccup)/float(sumhhold)),2) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
            area["areadata"]      = areadata
            area["data"]          = series.getlistTojson(dtlist,list1,"Date","Cost")
        else:
            area                  = None
        
        return area
            
    '''
    Analyse the night data of the household in the given dma
    dma:    Household in this DMA will be analyse to generate statistics
    period: periods in terms of number of months
    stdate: The start date of period to analyse if period is specified in range
    endate: The end date of period to analyse if period is specified in range
    return: If no data exists for the specified period or dates then return None other return statistics    
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()           
        >>> d.getnightstats(household_dma,12) #dma with household and period is 12 months
        or 
        >>> d.getnightstats(household_dma,"days","10-02-01","10-05-01") #dma with household and period is 12 months    
    '''
    def getnightstats(self,dma,period=0,stdate=None,endate=None):
        area = None
        areadata = {"sum":"","household":"","occupant":""}        
        dtlist = []
        list1 = []        
        day   = ""
        night = ""
        nightdata = {"max":"","min":"","sum":"","avg":""}
        #day,night = None, None
        count = 0
        sumnight = 0.0
        series   = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0        

        #if not days:  #period is specfied in months not in range
        if str(period)=="days":
            sdate     = iutility.convertdate(stdate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            edate     = iutility.convertdate(endate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            today     = iutility.getstrTodate(edate,"%Y-%m-%d") 
            #edate     = iutility.last_day_month(iutility.getstrTodate(edate,"%Y-%m-%d"))
            numdays   = iutility.diffdays(iutility.getstrTodate(edate,"%Y-%m-%d"),iutility.getstrTodate(sdate,"%Y-%m-%d"))  #number of days
            period    = iutility.diffmonth(iutility.getstrTodate(edate,"%Y-%m-%d"),iutility.getstrTodate(sdate,"%Y-%m-%d")) + 1 #number of months
            start     = iutility.subtract_year_month(today,month=period-1) #graph start date
            end       = today
        else:                
            '''
            extract the data specified in the period from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
            '''
            #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value            
            today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
            today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
            today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
            start = iutility.subtract_year_month(today,month=period-1) #graph start date 
            end   = today #graph end date
        
        sumonth = {}
        temp = start
        for x in range(0,period):
            sumonth[str(temp)] = 0.0
            #dtlist.append(str(temp))
            temp = iutility.addMonths(temp,1)
            
        temp = start
        
        for household in dma:
            
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if len(ts_monthly)<period: #if timeseries data is less than period
                continue
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"

            firstday = iutility.subtract_year_month(today,month=period-1)
            lastday  = iutility.last_day_month(today)
            pdfmonth = pdf[firstday:lastday]       
            months   = pdfmonth.count()
            #print months
            if months["units"]!=period: # data is less than required period so dont calculate value for this household    
                continue
            
            sumhhold = sumhhold + 1 #number of household
            sumoccup = sumoccup + household.num_of_occupants #number of occupants
             
            #hourly series for night data comparison  
            ts_hourly = series.readseries(series.gethourlyseries(household))
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_hourly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"            
            #replace all NAN with 0.0 to avoid messing up JSON at the client side
            pdf["units"].fillna(0.0,inplace=True)
            
            for x in range(int(period),0,-1): #decrement the loop so chart display starts from previous years
                firstday = iutility.subtract_year_month(today,month=(x-1))
                lastday  = iutility.last_day_month(firstday)
                pdfmonth = pdf[firstday:lastday]                            
                pdfnight = pdfmonth.between_time('18:00','06:00')
                
                #night values
                pdfnight   = np.sum(pdfnight.values) # sum all values
                unitshhold = unitshhold + pdfnight # sum of all units for every household
                sumonth[str(firstday)] = sumonth[str(firstday)] + pdfnight
         
        if sumhhold>0:
            temp = start
            for x in range(0,period):
                list1.append(sumonth[str(temp)]/sumhhold) 
                dtlist.append(str(temp)) 
                temp = iutility.addMonths(temp,1)
            
            areadata["sum"]       = unitshhold            
            areadata["household"] = unitshhold/sumhhold #units consume per household
            areadata["occupant"]  = areadata["household"]/(float(sumoccup)/float(sumhhold)) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants            
            area = series.getlistTojson(dtlist,list1,"date","units")
            area.append({"areadata":areadata})
   
        return area
    
    '''
    Analyse the day data of the household in the given dma
    dma:    Household in this DMA will be analyse to generate statistics
    period: periods in terms of number of months
    stdate: The start date of period to analyse if period is specified in range
    endate: The end date of period to analyse if period is specified in range
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()           
        >>> d.getperiodstatsefficient(household_dma,"10-02-2008","10-05-2008") #dma with household and period is 12 months
    '''
    def getperiodstatsefficient(self,dma,stdate,endate):
        #print period
        first = True
        area = {}
        areadata = {"sum":"","household":"","occupant":""}        
        dtlist = []
        list1 = []        
        day   = ""
        night = ""
        nightdata = {"max":"","min":"","sum":"","avg":""}
        #day,night = None, None
        count = 0
        sumnight = 0.0
        series   = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0   
        idx = 0
        value = 0.0
        occupants = 0
        today     = iutility.getstrTodate(endate,"%Y-%m-%d") 
        numdays   = iutility.diffdays(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d"))  #number of days
        period    = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1 #number of months
        start     = iutility.subtract_year_month(today,month=period-1) #graph start date
        end       = today
        
        sumonth = {}
        temp = start
        for x in range(0,period):
            sumonth[str(temp)] = 0.0
            temp = iutility.addMonths(temp,1)
            list1.append(0.0)
            
        temp = start
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if len(ts_monthly)<period:
                continue
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"

            firstday = iutility.subtract_year_month(today,month=period-1)
            lastday  = iutility.last_day_month(today)
            pdfmonth = pdf[firstday:lastday]       
            months   = pdfmonth.count()
            #print months
            if months["units"]!=period: # data is less than required period so dont calculate value for this household    
                continue

            #sumhhold = sumhhold + 1 #number of household
            #sumoccup = sumoccup + household.num_of_occupants #number of occupants
             
            idx = 0
            for x in range(int(period),0,-1): #decrement the loop so chart display starts from previous years
                firstday = iutility.subtract_year_month(today,month=(x-1))
                lastday  = iutility.last_day_month(firstday)
                if math.isnan(pdfmonth["units"][idx]):
                    continue
                if first:
                    occupants  = household.num_of_occupants
                    list1[idx] = pdfmonth["units"][idx]
                    first      = False
                else:
                    if list1[idx] == 0.0:
                        list1[idx] = pdfmonth["units"][idx]
                    else:
                        if pdfmonth["units"][idx] < list1[idx]:
                            list1[idx] = pdfmonth["units"][idx]
                        
                idx        = idx + 1

        
        #units  = [float(round(n, 2)) for n in mylist]
        if first==False:
            temp = start
            for x in range(0,period): 
                dtlist.append(str(temp)) 
                temp = iutility.addMonths(temp,1)
        
            mylist  = [float(round(n, 2)) for n in list1]
    
            areadata["sum"]       = sum(mylist)
            areadata["household"] = round(areadata["sum"],2) #each month represents 1 household and in every season there are months in total 
            areadata["occupant"]  = round(areadata["household"]/occupants,2) # this is the time
            area["data"]          = series.getlistTojson(dtlist,mylist,"date","units")
            area["areadata"]      = areadata
        else:
            area = None                
        
        return area
        
    '''
    Analyse the day data of the household in the given dma
    dma:    Household in this DMA will be analyse to generate statistics
    period: periods in terms of number of months
    stdate: The start date of period to analyse if period is specified in range
    endate: The end date of period to analyse if period is specified in range
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()           
        >>> d.getperiodstats(household_dma,"10-02-2008","10-05-2008") #dma with household and period is 12 months
    '''
    def getperiodstats(self,dma,stdate,endate):
        #print period
        area = {}
        areadata = {"sum":"","household":"","occupant":""}        
        dtlist = []
        list1 = []        
        day   = ""
        night = ""
        nightdata = {"max":"","min":"","sum":"","avg":""}
        #day,night = None, None
        count = 0
        sumnight = 0.0
        series   = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0   
        idx = 0
        value = 0.0
        
        #if not days:  #period is specfied in months not in range
        #if str(period)=="days":
            #sdate     = iutility.convertdate(stdate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
            #edate     = iutility.convertdate(endate,'%d-%m-%Y','%Y-%m-%d') #convert it into format suitable to extract data from dataframe
        today     = iutility.getstrTodate(endate,"%Y-%m-%d") 
            #edate     = iutility.last_day_month(iutility.getstrTodate(edate,"%Y-%m-%d"))
        numdays   = iutility.diffdays(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d"))  #number of days
        period    = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1 #number of months
        start     = iutility.subtract_year_month(today,month=period-1) #graph start date
        end       = today
        
        '''
        else:                
           
            extract the data specified in the period from the current date, excluding the current month as we will only analyse the things on the monthly basis for the whole calender month
           
            #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value            
            today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
            today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
            today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
            start = iutility.subtract_year_month(today,month=period-1) #graph start date 
            end   = today #graph end date        
        '''     
        #today = datetime.date.today() # commenting today's date because there is no timeseries data in DB for previous month but 2009 and 2010 data so assigning temporary value        
        #today = iutility.getstrTodate("2010-01-03","%Y-%m-%d") #temporary value 
        #today = iutility.subtract_year_month(today,month=1) #excluding current month of billing
        #today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d") #make sure start of the month
        #start = iutility.subtract_year_month(today,month=period-1) #graph start date 
        #end   = today #graph end date
        
        sumonth = {}
        temp = start
        for x in range(0,period):
            sumonth[str(temp)] = 0.0
            #dtlist.append(str(temp))
            temp = iutility.addMonths(temp,1)
            
        temp = start
        for household in dma:
            
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if len(ts_monthly)<period:
                continue
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"

            firstday = iutility.subtract_year_month(today,month=period-1)
            lastday  = iutility.last_day_month(today)
            pdfmonth = pdf[firstday:lastday]       
            months   = pdfmonth.count()
            #print months
            if months["units"]!=period: # data is less than required period so dont calculate value for this household    
                continue

            sumhhold = sumhhold + 1 #number of household
            sumoccup = sumoccup + household.num_of_occupants #number of occupants
             
            #hourly series for night data comparison  
            #ts_hourly = series.readseries(series.gethourlyseries(household))
            #get dates and values in a separate list
            #dates, units = IT.izip(*ts_hourly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            #pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            #pdf.index.name = "dates"            
            #replace all NAN with 0.0 to avoid messing up JSON at the client side
            #pdf["units"].fillna(0.0,inplace=True)
            idx = 0
            for x in range(int(period),0,-1): #decrement the loop so chart display starts from previous years
                firstday = iutility.subtract_year_month(today,month=(x-1))
                lastday  = iutility.last_day_month(firstday)
                pdfmonth["units"].fillna(0.0,inplace=True)
                #pdfmonth = pdf[firstday:lastday]                            
                #pdfnight = pdfmonth.between_time('07:00','17:00')
                
                #night values
                value      = pdfmonth["units"][idx]#np.sum(pdfnight.values) # sum all values
                idx        = idx + 1
                unitshhold = unitshhold + value # sum of all units for every household
                sumonth[str(firstday)] = sumonth[str(firstday)] + value
             
        if sumhhold>0:
            temp = start
            for x in range(0,period):
                list1.append(round(sumonth[str(temp)]/sumhhold,2)) 
                dtlist.append(str(temp)) 
                temp = iutility.addMonths(temp,1)
            
            areadata["sum"]       = round(unitshhold,2)            
            areadata["household"] = round(unitshhold/sumhhold,2) #units consume per household
            areadata["occupant"]  = round(areadata["household"]/(float(sumoccup)/float(sumhhold)),2) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants            
            area["data"]          = series.getlistTojson(dtlist,list1,"date","units")
            area["areadata"]      = areadata
        else:
            area = None
            
        return area
        
    '''
    analyse the household's summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> getwinterstats(household_dma,"2010")    
    '''
    def getwinterstats(self,dma,year):
        start = year+"-12-01"
        year  = str(int(year)+1)
        mid   = year+"-01-01"
        end   = year+"-02-01"
        area  = None
        areadata = {"sum":"","household":"","occupant":""}
        sumonth = {start:0.0,mid:0.0,end:0.0}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0
        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if not len(ts_monthly)>=3:  #Total three months in the winter
                continue
            
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"
             
            pdfsummer = pdf[start:end]
            months    = pdfsummer.count()
            if months["units"]==3: #if there are three winter months
                sumhhold = sumhhold + 1 #number of household
                sumoccup = sumoccup + household.num_of_occupants #number of occupants 
                #youdtlist = pdfsummer.index.values
                #youdtlist = [str(date.astype('M8[D]')) for date in youdtlist]
                list1          = pdfsummer.values
                sumonth[start] = sumonth[start] + list1[0]
                sumonth[mid]   = sumonth[mid]   + list1[1]
                sumonth[end]   = sumonth[end]   + list1[2]
                unitshhold = unitshhold + np.sum(list1) #sum of all units for every household
 
        
        if sumhhold>0:     
            list1[0] = sumonth[start]/sumhhold
            list1[1] = sumonth[mid]/sumhhold
            list1[2] = sumonth[end]/sumhhold    
            dtlist   = [start,mid,end]
            
            areadata["sum"]       = unitshhold
            
            areadata["household"] = unitshhold/sumhhold #units consume per household
            areadata["occupant"]  = areadata["household"]/(float(sumoccup)/float(sumhhold)) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
            area     = series.getlistTojson(dtlist,list1,"date","units")
            area.append({"areadata":areadata})
        
        return area
        
    '''
    analyse the summer data for the given dma and year
    dma:  Household in this DMA will be analyse to generate statistics
    year: This is the year to analyse the data
    return: If no data exists for the specified period or dates then return None other return statistics
        >>> d = idma()
        >>> dma = DMA.objects.get(pk=10) 
        >>> household_dma = dma.households.all()        
        >>> getsummerstats(household_dma,"2010")    
    '''
    def getsummerstats(self,dma,year):
        start = year+"-06-01"
        mid   = year+"-07-01"
        end   = year+"-08-01"
        area  = None
        areadata = {"sum":"","household":"","occupant":""}
        sumonth = {start:0.0,mid:0.0,end:0.0}
        series = iseries()
        sumhhold = 0
        sumoccup = 0
        unitsoccup = 0.0
        unitshhold = 0.0
        sumunitshhold = 0.0
        #process every household
        for household in dma:
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            if not len(ts_monthly)>=3: #Three months in the summer 
                continue
            
            #get dates and values in a separate list
            dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
            #create pandas Series (time series using two different list for timeseries data analysis
            pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
            pdf.index.name = "dates"
             
            pdfsummer = pdf[start:end]
            months    = pdfsummer.count()
            if months["units"]==3: #if there are three summer months
                sumhhold = sumhhold + 1 #number of household
                sumoccup = sumoccup + household.num_of_occupants #number of occupants 
                #youdtlist = pdfsummer.index.values
                #youdtlist = [str(date.astype('M8[D]')) for date in youdtlist]
                list1          = pdfsummer.values
                sumonth[start] = sumonth[start] + list1[0]
                sumonth[mid]   = sumonth[mid]   + list1[1]
                sumonth[end]   = sumonth[end]   + list1[2]
                unitshhold = unitshhold + np.sum(list1) #sum of all units for every household
 
        
        if sumhhold>0:
            list1[0] = sumonth[start]/sumhhold
            list1[1] = sumonth[mid]/sumhhold
            list1[2] = sumonth[end]/sumhhold
            dtlist = [start,mid,end]
            
            areadata["sum"]       = unitshhold
            areadata["household"] = unitshhold/sumhhold #units consume per household
            areadata["occupant"]  = areadata["household"]/(float(sumoccup)/float(sumhhold)) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
            area     = series.getlistTojson(dtlist,list1,"date","units")
            area.append({"areadata":areadata})
        
        return area
    '''
    This methods returns statistics of the DMA
    dma: DMA model object
    month: Number of months of timeseries to analysis for DMA, this make sure that comparison only made for equal number of months
    '''
    def getStats(self,dma,months=12):
        sum_units = 0.0 #total units consumed by all households in DMA
        min_units = 0.0 #min units consumed by household in DMA
        max_units = 0.0 #max units consumed by household in DMA
        sum_households = 0 #total household in DMA
        sum_occupants = 0 #total occupants in DMA
        min_occupants = 0 #minimum number of occupants in household in DMA
        max_occupants = 0 #maximum number of occupants in household in DMA
        avg_occupants = 0 #average number of occupants per household in DMA
        sum_months = 0    #for calculating average bill per month per household when series intervals are irregular (such as when months=0)
        avg_units = 0.0
        count = 0     
           
        series = iseries()
        
        #these are the properties inside dictionary that will be computed for DMa model object
        dict = {"sum_households":"","sum_occupants":"","sum_units":"","max_occupants":"","avg_occupants":"","min_occupants":"","max_units":"","avg_units":"","min_units":"","occupant":""}
        
        for household in dma: #get every household
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            length = len(ts_monthly) #check timeseries months
            # Added by Chris Pantazis. Read comment in line 889!
            sum_households += 1  # total household in DMA
            temp = household.num_of_occupants
            sum_occupants = sum_occupants + temp #total occupants in DMA
            if length >= months: #if timeseries months greater that months, default is 12
                # Changed by Chris Pantazis
                # Again, like sum_households. This variable should be moved
                # outside of "IF" statement
                #temp = household.num_of_occupants
                if months==0: #this is for doing all users in DMA irrespect of any period, >0 period means hat calculation consider all household with range of months of units  
                    avg_units = avg_units + series.getAvg(ts_monthly,length) #average units/ per month
                else:
                    ts_monthly= ts_monthly[length-months:]

                # Change by Chris Pantazis on 24/09/2014.
                # Households and occupants should be increased
                # before the "IF" statement
                # because if months < 12 then it gives 0 to all those vars
                #sum_households= sum_households + 1 #total household in DMA
                #sum_occupants = sum_occupants + temp #total occupants in DMA

                sum_units     = sum_units + series.getSum(ts_monthly) #total units in DMA

                #finding minimum number of occupants
                if count==0:
                    min_occupants = temp
                else:
                    if temp < min_occupants:
                        min_occupants = temp
    
                #finding maximum number of occupants
                if count==0:
                    max_occupants = temp
                else:
                    if temp > max_occupants:
                        max_occupants = temp
                                                    
                #finding lowest units in household                                                        
                temp = series.getLowest(ts_monthly)
                temp = temp[0]['unit']
                if count==0:
                    min_units = temp
                else:
                    if temp < min_units: 
                        min_units = temp
                        
                #finding highest units in household
                temp = series.getHighest(ts_monthly)
                temp = temp[0]['unit']
                if count==0:
                    max_units = temp
                else:
                    if temp > max_units: 
                        max_units = temp
                
                count = count + 1
        
        dict["sum_households"]= round(sum_households,2)  
        dict["sum_occupants"] = round(sum_occupants,2)
        dict["sum_units"]     = round(sum_units,2)
        dict["max_units"]     = round(max_units,2)
        if months==0:
            dict["avg_units"] = round(avg_units/sum_households,2) #average units consumed by household in DMA per month
        else:
            dict["avg_units"] = round(sum_units/sum_households,2) #average units consumed by household in DMA 
        dict["min_units"]     = round(min_units,2)
        dict["max_occupants"] = round(max_occupants,2)        
        dict["avg_occupants"] = round(float(sum_occupants)/float(sum_households),2) #average number of occupants per household in DMA
        dict["min_occupants"] = round(min_occupants,2)
        dict["occupant"]      = round(dict["avg_units"]/dict["avg_occupants"],2) #units consume per household / (sumoccup/sumhhold : average occupants per household = average units consume per occupants
        return dict

    '''
    This methods returns statistics of the DMA
    dma: DMA model object
    month: Number of months of timeseries to analysis for DMA, this make sure that comparison only made for equal number of months
    '''
    def gethouseholdstats(self,dma,months=12):
        sum_units = 0.0 #total units consumed by all households in DMA
        min_units = 0.0 #min units consumed by household in DMA
        max_units = 0.0 #max units consumed by household in DMA
        sum_households = 0 #total household in DMA
        sum_occupants = 0 #total occupants in DMA
        sum_months = 0    #for calculating average bill per month per household when series intervals are irregular (such as when months=0)
        avg_units = 0.0
        count = 0     
           
        series = iseries()
        
        #these are the properties inside dictionary that will be computed for DMA model object
        dict = {"sum_households":"","sum_occupants":"","sum_units":"","max_units":"","avg_units":"","min_units":""}
        
        for household in dma: #get every household
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            length = len(ts_monthly) #check timeseries months
            if length>=months: #if timeseries months greater that months, default is 12
                temp          = household.num_of_occupants
                if months==0: #this is for doing all users in DMA irrespect of any period, >0 period means hat calculation consider all household with range of months of units  
                    avg_units = avg_units + series.getAvg(ts_monthly,length) #average units/ per month
                else:
                    ts_monthly= ts_monthly[length-months:]
                     
                sum_households= sum_households + 1 #total household in DMA
                sum_occupants = sum_occupants + temp #total occupants in DMA
                sum_units     = sum_units + series.getSum(ts_monthly) #total units in DMA

                #finding lowest units in household                                                        
                temp = series.getLowest(ts_monthly)
                temp = temp[0]['unit']
                if count==0:
                    min_units = temp
                else:
                    if temp < min_units: 
                        min_units = temp
                        
                #finding highest units in household
                temp = series.getHighest(ts_monthly)
                temp = temp[0]['unit']
                if count==0:
                    max_units = temp
                else:
                    if temp > max_units: 
                        max_units = temp
                
                count = count + 1
        
        dict["sum_households"]= sum_households  
        dict["sum_occupants"] = sum_occupants
        dict["sum_units"]     = sum_units
        dict["max_units"]     = max_units
        if months==0:
            dict["avg_units"] = avg_units/sum_households #average units consumed by household in DMA per month
        else:
            dict["avg_units"] = sum_units/sum_households #average units consumed by household in DMA
        dict["min_units"]     = min_units        
        
        return dict   
    
    '''
    This method returns the most efficient user of the DMA
    dma: DMA model object
    month: Number of months of timeseries to analysis for DMA, this make sure that comparison only made for equal number of months    
    '''
    def getMostefficient(self,dma,months=12):
        months     = {}
        curmonths  = 0.0
        series     = iseries()
        hhold      = Ihousehold.ihousehold()
        curunits   = {}
        zero       = True
        list1 = []
        data = {}
        packdata = {}
        monthunits = {}
        #dic12 = {"period":"","sum_units":"","avg_units":"","unit_person":""}
        dic12 = {}
        effdata = {}#"12 Month":"","6 Month":"","3 Month":"","1 Month":""}
        occupants = 0
        for household in dma: #get every household
            ts_monthly = series.readseries(series.getmonthlyseries(household)) #get timeseries
            length = len(ts_monthly) #check timeseries months
            idx    = 1
            if length>=12:
                for x in range(0, 4):
                    months[str(idx)] = ts_monthly[length-idx:]
                    dates, units     = IT.izip(*months[str(idx)]) #much better for longer data, returning tuples
                    if zero:
                        monthunits[str(idx)] = sum(units)
                    else:
                        curmonths    = sum(units)
                        if curmonths < monthunits[str(idx)]: # if current user months usage is less than update
                            monthunits[str(idx)] = curmonths
                    #make sure to set zero at the end of first user
                    if idx==12:
                        if zero:
                            occupants = household.num_of_occupants
                            zero = False
                            
                    if idx==1:
                        idx = idx + 2
                    else:
                        idx = idx + idx
        
        if len(monthunits) > 0:
            idx = 1
            for x in range(0, 4):
                data["Units"] = round(monthunits[str(idx)],2)
                data["Cost"]  = round(hhold.tariff1(monthunits[str(idx)]),2)
                data["Period"]= str(idx)+" Month"
                data["Data"]  = "Most Efficient"
                
                list1.append(data)
                
                dic12["sum_units"]   = data["Units"] 
                dic12["period"]      = data["Period"]
                dic12["unit_person"] = round(dic12["sum_units"]/occupants,2)
                effdata[str(idx)+" Month"] = dic12
                
                dic12= {}
                data = {}
                
                if idx==1:
                    idx = idx + 2
                else:
                    idx = idx + idx
             
            packdata["chartdata"] = list1
            packdata["stats"]     = effdata
        else:
            packdata = None
        
        return packdata