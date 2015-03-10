'''
Created on 24 Feb 2014
@author: adeel
'''
import datetime
import time
import pandas as pd
import numpy as np
import itertools as IT
from dateutil import parser
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from py4j.java_gateway import JavaGateway, GatewayClient
from django.db import connection
from unexe.models import *
import json, urlparse, traceback
from classes.Iuser import iuser
from classes.Iutility import iutility
from classes.Ihousehold import ihousehold
from classes.Iforecast import iforecast
from classes.Iseries import iseries
from classes.Ifile import ifile
from classes.Idma import idma
from classes.Ierror import ierror
from classes.Iemail import iemail
from classes.Iusecase import iusecase
from classes.Iconfig import iconfig
from classes.Irest import irest
from enhydris.hcore.views import (TimeseriesDetailView as TDV,
        bufcount)
from enhydris.hcore.models import Timeseries, Gentity, Garea
from enhydris.conf import settings
from iwidget.models import (IWTimeseries, Household, DMA, PropertyType,
        TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY, TSTEP_MONTHLY,
        VAR_CUMULATIVE, VAR_PERIOD, VAR_COST, TSTEP_HOURLY,UserProfile)
from iwidget.utils import statistics_on_daily
from pthelma.timeseries import Timeseries
from enhydris.hcore.models import ReadTimeStep
from django.db.models import Avg,Max,Min,Count,Sum
from enhydris.settings import SSO_APP
#from enhydris.hcore.models import (Lookup as HLookup, Timeseries, Gpoint,
#        Garea, Instrument)
# added some comments!

#from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext as _

'''
This method return the webpage of UK Case study registration page
'''
class ukcsregistration(TemplateView):
    template_name = "casestudy/ukcsregistration.html"

    def get(self, request):
        #if request.user.is_authenticated(): #if already authenticated
        #    return redirect(reverse('dashboard'))   #redirect to a dashboard
        return self.render_to_response({})

class ukcsregistrationconfirm(TemplateView):
    template_name = "casestudy/ukcsregistrationconfirm.html"

    def get(self, request):
        #if request.user.is_authenticated(): #if already authenticated
        #    return redirect(reverse('dashboard'))   #redirect to a dashboard
        return self.render_to_response({})
'''
This method captures the UK case study form page data, verify the details, 
store the user details in DB and UPL web service and send confirmation email. 
Following status message this method return
Successfully register: True
Already activate: -1
Address not found: -2
Unexpected Error: False - should be inside try block
'''
class ukcsregistrationsave(TemplateView):
    template_name = "casestudy/ukcsregistration.html"

    def post(self, request):
        status   = 0
        fname    = iutility.getPostValue('ukcsregfname',request).strip()
        lname    = iutility.getPostValue('ukcsreglname',request).strip()
        email    = iutility.getPostValue('ukcsregemail',request).strip()
        addr     = iutility.getPostValue('ukcsregaddress',request).strip()
        profile  = None
        
        #user class
        wuser = iuser()
        #rest class
        #rest  = irest(iconfig.UPLWSServer,iconfig.UPLWSUsername,iconfig.UPLWSPassword)
        
        try:
            profile = UserProfile.objects.get(address__iexact=addr)
        except:
            status  = ierror.NOT_FOUND
        
        if profile:            
            if profile.user.is_active is False:
                if not fname == "":
                    profile.user.first_name = fname
                if not lname == "":
                    profile.user.last_name  = lname
                
                username = wuser.getUsername(email.split('@')[0])
                password = wuser.getPassword()    
                
                #print username
                #rest.addUser(username,password)
                #print rest.getUser(username)
                profile.user.username = username #set username
                profile.user.email = email          #set email
                profile.user.set_password(password) #set password                
                #profile.user.is_active = True       #set active user
                profile.user.is_staff = False
                
                #send email
                content = "Here is your account details:\nUsername: "+username+"\nPassword: "+password+"\n\niWIDGET Weblink: "+iconfig.iWIDGETURL
                mail = iemail(email,"iWIDGET Account",content)
                mail.sendEmail()

                #finally save profile
                profile.user.save()
                
                status = True
            else:
                status = ierror.ALREADY_EXIST

        return HttpResponse(json.dumps(status),content_type='application/javascript')
    
class test(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return HttpResponseRedirect('https://services.up-ltd.co.uk/iwidget/Login.aspx?c=NTUA')
        #if request.user.is_authenticated(): #if already authenticated
        #    return redirect(reverse('dashboard'))   #redirect to a dashboard
        return self.render_to_response({})

class home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        # Added by Chris Pantazis on 14/10/2014
        # in order to pre-fillin the username in the username field
        # in case of readirection (e.g. after SSO or custom sign-in
        # process. We might not need it in the end, but it is good to
        # have the option
        username = request.GET.get('u', '')
        if request.user.is_authenticated(): #if already authenticated
            return redirect(reverse('dashboard'))   #redirect to a dashboard
        return redirect(reverse("login"))

class login(TemplateView):
    template_name = "index.html"

    def post(self, request):
        wuser = iuser()        
        status = wuser.login(iutility.getPostValue('username',request), iutility.getPostValue('password',request), request)
        #    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponse(json.dumps(status),content_type='application/javascript')
        #else:
        #    return super_index(request)            
        #return self.render_to_response({})
    
#class logout(TemplateView):
#    template_name = "index.html"
#
#    def get(self, request):
#        auth_logout(request)
#        return redirect(reverse('home'))   #redirect to home page
#        return self.render_to_response({})

# Added by Chris Pantazis in order for the user to logout
# and get redirected to SSO login page
class logout(TemplateView):
    template_name = ""

    def get(self, request):
        auth_logout(request)
        return HttpResponseRedirect("https://services.up-ltd.co.uk/iwidget/?c=%s" % SSO_APP)

#change user password
class changepassword(TemplateView):
    template_name = "dashboard.html"

    def post(self, request):
        if request.user.is_authenticated(): #only change password if authenticated
            wuser = iuser()
            status = wuser\
                .changepassword(request.user,
                                iutility.getPostValue('oldpasswd', request),
                                iutility.getPostValue('newpasswd', request))
            # Added by Chris Pantazis to change password to UPL, too
            if status:
                from sso.common import encrypt_and_hash_pwd
                import requests
                from xml.dom import minidom
                xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><SetUserPassword xmlns="https://services.up-ltd.co.uk/adminservice_iwidget/"><name>##USER##</name><password>##PASSWORD##</password><serviceUsername>IWidgetService</serviceUsername><servicePassword>1-Widg3t##Crypt0Service</servicePassword></SetUserPassword></soap:Body></soap:Envelope>"""
                new_pwd = iutility.getPostValue('newpasswd', request)
                enc_pwd = encrypt_and_hash_pwd(new_pwd)
                xml = xml.replace("##USER##", request.user.username)\
                    .replace("##PASSWORD##", enc_pwd)
                headers = {'Content-Type': 'text/xml'}
                res = requests.post('https://services.up-ltd.co.uk/'
                                    'adminservice_iwidget/service.asmx',
                                    data=xml, headers=headers)
                if res.status_code == requests.codes.ok:
                    doc = minidom.parseString(res.text)
                    result = doc.getElementsByTagName("SetUserPasswordResult")[0]
                    val = result.firstChild.data
                    if val == "true":  # True only if SSO update was OK!!
                        status = True
                        try:
                            uvk = UserValidationKey.\
                                objects.get(user=request.user)
                            uvk.key = new_pwd
                            uvk.save()
                        except UserValidationKey.DoesNotExist:
                            uvk = UserValidationKey. \
                                objects.create(user=request.user,
                                               identifier="",
                                               key=new_pwd,
                                               sso=True,
                                               popup=False)
                    else:
                        status = False
            return HttpResponse(json.dumps(status),content_type='application/javascript')
        else:   #otherwise return -1 to show unexpected error message
            return HttpResponse(json.dumps(-1),content_type='application/javascript')
  
#update user profile
class updateuser(TemplateView):
    template_name = "dashboard.html"

    def post(self, request):
        if request.user.is_authenticated(): #only update user if authenticated
            qs     = iutility.getPostqs(request)    #get quertystring
            values  = dict(urlparse.parse_qsl(qs)) #parse qs values into dictonary
            wuser = iuser()
            return HttpResponse(json.dumps(wuser.updateuser(request.user,values)),content_type='application/javascript')
        else:   #otherwise return -1 to show unexpected error message
            return HttpResponse(json.dumps(-1),content_type='application/javascript')

#this class return serialize json object to be process by client side (browser)
class getuser(TemplateView):
    template_name = "dashboard.html"

    def post(self, request):
        if request.user.is_authenticated(): #only update user if authenticated
            wuser = iuser() #user class object
            return HttpResponse(json.dumps(wuser.getuser(request.user)),content_type='application/javascript')
        else:   #otherwise return -1 to show unexpected error message
            return HttpResponse(json.dumps(-1),content_type='application/javascript')

#this class return serialize json object to be process by client side (browser)
class gethousehold(TemplateView):
    template_name = "dashboard.html"
    
    def post(self, request):
        if request.user.is_authenticated(): #only update user if authenticated         
            whousehold = ihousehold() #household class object
            whousehold.getHouseholdData()
            val=None
            val = iutility.getPostValue("id",request)
            if val=="None":
                val=None
            return HttpResponse(json.dumps(whousehold.gethousehold(request.user,val)),content_type='application/javascript')
        else:   #otherwise return -1 to show unexpected error message
            return HttpResponse(json.dumps(-1),content_type='application/javascript')
        

#this class return serialize json object to be process by client side (browser)
class updatehousehold(TemplateView):
    template_name = "dashboard.html"

    def post(self, request):
        if request.user.is_authenticated():  # only update user if authenticated
            whousehold = ihousehold()  # household class object
            qs = iutility.getPostqs(request)  # get quertystring
            values = dict(urlparse.parse_qsl(qs))  # parse qs values into dictonary
            if whousehold.updatehousehold(request.user, values):
                ans = _("Your household profile has updated successfully")
            else:
                ans = _("There was an error. Please contact the Administrator")
            return HttpResponse(json.dumps(ans),
                                content_type='application/javascript')
        else:  # otherwise return -1 to show unexpected error message
            # print "request.user.is_authenticated(): FALSE"
            ans = _("You are not authorised to update data")
            return HttpResponse(ans,
                                content_type='application/javascript')


#Template class for super user profile and password update
class usersuper(TemplateView):
    template_name = "usersuper.html"
        
    def get(self,request,**kwargs):
        return self.render_to_response({})

#Template class for super user main page
class superuser(TemplateView):
    template_name = "superusers.html"
        
    def get(self,request,**kwargs):
        return self.render_to_response({})

#TemplateView class for consumer dashboard                                                                  
class consumer(TemplateView):
    template_name = "dashboard.html"
    
    '''
    This method only executed if the logged user is not superuser or staff privelege level
    If entered into method when logged in as super user then unexpected error might result.
    This error needs to fix as well..
    '''
    def get(self,request,**kwargs):
        #following code is to do with use case developed by NTUA
        from iwidget.views import dashboard_view
        try:
            hid = self.kwargs['household_id']
        except:
            hid = None        
            
        values = dashboard_view(request,hid) #call method from django_iwidget. sometimes I need to replace this
        household = values['household']

        # Added by Chris Pantazis because I was getting a
        # tsid template (UC4.1) error in superuser's dashboard
        # So I had to add tsid value to the dictionary.

        series = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_month = series.readseries(ts_monthly)
        ###
        if ts_monthly:
            ys = series.getstdate(timeseries_month).year
            ye = series.getendate(timeseries_month).year
            yearlist = []
            while ys <= ye:
                yearlist.append(ys)
                ys += 1
        else:
            yearlist = []
        #end of NTUA use case
        # overview_nrg added by Chris Pantazis
        # to show Energy Consumption in Dashboard
        # Remeber this data dict goes to the dashboard
        data = {
            "yearlist": yearlist,
            "household": household,
            "overview": values['overview'],
            "overview_nrg": values['overview_nrg'],
            "has_energy": values['has_energy'],
            'charts': values["charts"],
            'charts_nrg': values["charts_nrg"],
            'js_data': values["js_data"],
            'chart_selectors': values["chart_selectors"],
            "hid": hid,
            "tsid": ts_monthly.id,
        }
        
        ##start of my code
        user = request.user
        #only execute these use cases if logged user is not admin
        if not (user.is_staff or user.is_superuser):
            usecase= iusecase(user)
            series = iseries()
            household = user.households.all()[0]
            
            '''
            following code is to do with forecasting use case 5.3
            '''
            months = 12
            #monthly series
            ts_monthly = series.getmonthlyseries(household)
            timeseries_month = series.readseries(ts_monthly)

            ts_monthlyid = ts_monthly.id
            #daily series
            ts_daily = series.getdailyseries(household)
            timeseries_daily = series.readseries(ts_daily)
            
            #get start and end date of consumer timeseries or date
            stdate = series.getstdate(timeseries_daily)
            endate = series.getendate(timeseries_daily)
            stdate = iutility.convertdate(str(stdate),'%Y-%m-%d','%d-%m-%Y')
            endate = iutility.convertdate(str(endate),'%Y-%m-%d','%d-%m-%Y')
            
            #hourly series
            '''
            ts_hourly = series.gethourlyseries(household)
            timeseries_hourly = series.readseries(ts_hourly)
            dates, units = IT.izip(*timeseries_hourly) #much better for longer data
            f =  pd.Series(units,index=dates)
            today = datetime.date.today()
            today = iutility.getstrTodate(str(today.year)+"-"+(today.strftime("%m"))+"-01","%Y-%m-%d")
            finish= iutility.subtract_year_month(today,month=1)
            start = iutility.subtract_year_month(today,month=4)
            print finish
            print start
            '''
            # Removed by DJW for login optimisation.
            #c_uc52data = usecase.usecase5_2()
            
            c_uc53data = usecase.usecase5_3(user,timeseries_month,timeseries_daily) ##use case 5.3
            
            '''
            
            if length>12:
                tseries_month = timeseries_month[length-months:] #get the latest last 12 months
            sum  = series.getCost(series.getSum(tseries_month))
            high = json.dumps(series.getHighestCost(tseries_month)) #still need to write function to get cost
            low  = json.dumps(series.getLowestCost(tseries_month))  #still need to write function to get cose
            avg  = series.getCost(series.getAvg(tseries_month,len(tseries_month)))
            tsmonth = json.dumps(series.getseriesTojsoncost(tseries_month,"cost"))
            end of the code for use case 5.3
            '''
            
            # Removed by DJW for login optimisation.
            #
            #'''
            #code for use case 3.2 - compare consumer with other consumer in the same area or building or neighbour
            #'''
            #c_uc32data = usecase.usecase3_2()
            #dmasummary = ""            
            #'''
            #Default chart for showing on selection of tab.
            #
            #length = len(timeseries_month)
            #dma = household.dma
            #dmastats = DMAstats.objects.filter(dma__pk=dma.pk) #make sure to get the latest DMA stats by reading again from database in case values updated 
            #obj = {}
            #list1 = []
            #for st in dmastats:
            #    #getting DMA status for the average unit/bill
            #    obj["Units"] = str(st.avgunits)
            #    obj["Cost"]  = str(series.getCost(st.avgunits))
            #    obj["Period"]= str(st.statsperiod)+" Month"
            #    obj["Data"]  = "DMA"
            #    list1.append(obj)
            #    obj = {}
            #    tseries      = timeseries_month[length-st.statsperiod:]
            #    obj["Units"] = str(series.getSum(tseries))
            #    obj["Cost"]  = str(series.getCost(float(obj["Units"])))
            #    obj["Period"]= str(st.statsperiod)+" Month"
            #    obj["Data"]  = "You"
            #    list1.append(obj)
            #    obj = {}
            #    
            #end of use case 3.2 code
            #'''     


            # Removed by DJW for login optimisation.
            #
            #'''
            #code for use case 3.3 - compare consumer with other consumer in the same area or building or neighbour
            #'''            
            #c_uc33data = usecase.usecase3_3()
            #'''
            #end of use case 3.3 code
            #'''
            ##"tsmonth":tsmonth,"high":high,"low":low,"sum":sum,"avg":avg,
            
            '''
            code for use case 3.4
            ''' 
            c_uc34data = usecase.usecase3_4()
            print "c_uc34data", c_uc34data
            '''            
            End of use case 3.4
            '''
            
            '''
            code for use case 4.1
            ''' 
            c_uc41data = usecase.usecase4_1()
            '''            
            End of use case 4.1
            '''
            
            '''
            code for use case 5.4
            '''
            usecase.usecase5_4()
            '''
            End of use case 5.4
            '''
            
            '''
            code for use case 5.4
            ''' 
            c_uc54data = None
            '''            
            End of use case 5.4
            '''
                                    
            #data = {"household":household,"tsmonth":tsmonth,"high":high,"low":low,"sum":sum,"avg":avg,"tsid":ts_monthly.id,"dmastats":dmasummary,"uc32chart1":json.dumps(list1),"dmastats":dmastats,}    
            # overview_nrg added by Chris Pantazis
            # various consumer lists and values added by David Walker
            # to show Energy Consumption in Dashboard
            # All those data go to the Dashboard! Oh yes!
            checkboxes, selects = ihousehold.getHouseholdData(household.id)
            data = {
                "allowed_plegma_users": ["GR006047"],
                "prefix": user.username[0:2],
                "list_100": range(101),
                "water_pricing_list": zip(range(1, 8), [_("Flat rate tariff"),
                                                        _("Water metering tariff"),
                                                        _("Rising block tariff"),
                                                        _("Declining block tariff"),
                                                        _("Seasonal tariff"),
                                                        _("Time-of-day tariff"),
                                                        _("Social tariff")]),
                "property_type_list" :  zip(range(1,5), [_("Detached"), _("Semi Detached"), _("Flat"), _("Tenement")]),
                "construction_period_list" : zip(range(1,5), [_("Before 1970"), "1971-1990", "1991-2000", _("After 2001")]),
                "ownership_status_list" : zip(range(1,3), [_("Owned"),_("Rented")]),
                "property_area_list" : zip(range(1,5), ["<= 50","51 - 100", "101 - 200", "> 200"]),
                "garden_area_list" : zip(range(1,5), ["<= 20","21 - 50", "51 - 100", "> 100"]),
                "pervious_area_list" : zip(range(1,5), ["<= 20","21 - 50", "51 - 70", "> 70"]),
                "roof_area_list" : zip(range(1,5), ["<= 50","51 - 100", "101 - 200", "> 200"]),
                "checkboxes" : checkboxes,
                "selects" : selects,
                "household": household,
                "yearlist": yearlist,
                "overview": values['overview'],
                "overview_nrg": values['overview_nrg'],
                "has_energy": values['has_energy'],
                'charts': values["charts"],
                'charts_nrg': values["charts_nrg"],
                'js_data': values["js_data"],
                'chart_selectors': values["chart_selectors"],
                "hid": hid,
                "tsid": ts_monthlyid,
                "stdate": stdate,
                "endate": endate,
                #"c_uc32data": json.dumps(c_uc32data),  # Removed by DJW. UCs 3.2, 3.3, 5.2 and 5.3 low load their
                #"c_uc33data": json.dumps(c_uc33data),  # data as and when it's needed with a separate call.
                "c_uc34data": json.dumps(c_uc34data),                
                "c_uc41data": json.dumps(c_uc41data),
                #"c_uc52data": json.dumps(c_uc52data),
                #"c_uc53data": json.dumps(c_uc53data),
                "c_uc54data": json.dumps(c_uc54data)}
 
        return self.render_to_response(data)            

'''
TemplateView class for consumer use case 3.4
'''
class c_uc34(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        comparechart=[{"Units":"","Data":"Efficient User"},{"Units":"","Data":"You"}]
        compare = iutility.getPostValue("compare",request)
        year    = iutility.getPostValue("year",request)
        period  = iutility.getPostValue("period",request)        
        #season  = iutility.getPostValue("season",request) 
        #season  = iutility.getPostValue("season",request)
        
        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id        

        d = idma() #class with dma related calcualtion
        
        #dma that will use for comparison
        dma  = household.dma  #get dma of the user
        #dma = DMA.objects.get(pk=11) #chosing other DMA for comparison, we will change this when we will get the different demographic database
        household_dma = dma.households.filter(num_of_occupants=household.num_of_occupants,property_type=household.property_type)        
        
        #hourly series
        series     = iseries()
        ts_monthly = series.readseries(series.getmonthlyseries(household))
        #timeseries_monthly = series.readseries(ts_monthly)
        
        hhold = ihousehold()
        #print hhold.getseasonusage(user,year,compare)    
        '''
        We will only perform the following operation if the timeseries_hourly has sufficient data for analysis.
        If there is not sufficient data then simply return nothing and deal with client side. At the moment there
        is no check in the development environment as we know there are plenty of data for analysis
        '''
        #get dates and values in a separate list
        dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
        #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        data = {}

        if period=="season":
            data["you"]  = hhold.getseasonusage(user,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            data["area"] = d.getseasonusagefficient(household_dma,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]
        elif period=="days": #if period is defined in range
            stdate       = iutility.getPostValue("stdate",request)
            endate       = iutility.getPostValue("endate",request)
            data["you"]  = hhold.getperiodstats(user,stdate,endate)
            data["area"] = d.getperiodstatsefficient(household_dma,stdate,endate)
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]                     
        else:
            data["you"]  = hhold.getmonthlyusage(user,int(period))
            data["area"] = d.getmonthlyusagefficient(household_dma,int(period))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]
                        
        if not data["you"] or not data["area"]:
            data = None
        else:
            #data["donutchart"] = donutchart
            data["comparechart"] = comparechart
        
        return HttpResponse(json.dumps(data),content_type='application/javascript')

'''
TemplateView class for consumer use case 4.1
'''
class c_uc41(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        data = None            
        return HttpResponse(json.dumps(data),content_type='application/javascript')

'''
TemplateView class for consumer use case 5.4
'''                                                                  
class c_uc54(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        data = None            
        return HttpResponse(json.dumps(data),content_type='application/javascript')
    
    
    
    
    
def tsMonthlyIdFromUser(user):
    """
    Helper function to avoid excessively repetetive code.
    @author: David Walker
    @date: 08/02/2015
    """
    series = iseries()
    household = user.households.all()[0]
    ts_monthly = series.getmonthlyseries(household)
    timeseries_month = series.readseries(ts_monthly)
    return ts_monthly.id
    
    
def uc_03_2(request):
    """
    Sub-template view for consumer use case 3.2.
    @author: David Walker
    @date: 06/02/2015
    """
    user = request.user
    ts_monthlyid = tsMonthlyIdFromUser(user)
    
    usecase = iusecase(user)
    c_uc32data = usecase.usecase3_2()
    
    data = {
        "c_uc32data": json.dumps(c_uc32data),
        "tsid" : ts_monthlyid
    }
    
    variables = RequestContext(request, data)
    return render_to_response("usecase/inner_c_uc3.2.html", variables)


def uc_03_2_compare(request):
    """
    Sub-template view for consumer use case 3.2.
    @author: David Walker
    @date: 06/02/2015
    """
    variables = RequestContext(request, {"tsid" : tsMonthlyIdFromUser(request.user)})
    return render_to_response("usecase/inner_c_uc3.2_compare.html", variables) 


def uc_03_3(request):
    """
    Sub-template view for consumer use case 3.3.
    @author: David Walker
    @date: 09/02/2015
    """
    user = request.user
    ts_monthlyid = tsMonthlyIdFromUser(user)
    
    usecase = iusecase(user)
    c_uc33data = usecase.usecase3_3()  
    
    data = {
        "c_uc33data" : json.dumps(c_uc33data),
        "tsid" : ts_monthlyid
    }
    
    variables = RequestContext(request, data)
    return render_to_response("usecase/inner_c_uc3.3.html", variables)


def uc_03_3_compare(request):
    """
    Sub-template for consumer use case 3.3.
    @author: David Walker
    @date: 09/02/2015
    """
    variables = RequestContext(request, {"tsid" : tsMonthlyIdFromUser(request.user)})
    return render_to_response("usecase/inner_c_uc3.3_compare.html", variables)


def uc_03_4(request):
    """
    Sub-template for consumer use case 3.4.
    @author David Walker
    @date: 10/03/2015
    """
    variables = RequestContext(request, {})
    return render_to_response("usecase/inner_c_uc3.4.html", variables)


def uc_04_1(request):
    """
    Sub-template for consumer use cases 4.1/5.4.
    @author David Walker
    @date: 10/03/2015
    """
    variables = RequestContext(request, {})
    return render_to_response("usecase/inner_c_uc4.1.html", variables)


def uc_05_2(request):
    """
    Sub-template for consumer use case 5.2.
    @author: David Walker
    @date: 09/02/2015
    """
    user = request.user
    ts_monthlyid = tsMonthlyIdFromUser(user)
    
    usecase = iusecase(user)
    c_uc52data = usecase.usecase5_2()
    
    data = {
        "c_uc52data" : json.dumps(c_uc52data),
        "tsid" : ts_monthlyid
    }
    
    variables = RequestContext(request, data)
    return render_to_response("usecase/inner_c_uc5.2.html", variables)


def uc_05_3(request):
    """
    Sub-template for consumer use case 5.3.
    @author: David Walker
    @date: 09/02/2015
    """
    user = request.user
    
    series = iseries()
    household = user.households.all()[0]
    ts_monthly = series.getmonthlyseries(household)
    timeseries_month = series.readseries(ts_monthly)
    
    ts_daily = series.getdailyseries(household)
    timeseries_daily = series.readseries(ts_daily)
    
    c_uc53data = usecase.usecase5_3(user, timeseries_month, timeseries_daily)
    
    data = {
        "c_uc53data" : c_uc53data,
        "tsid" : ts_monthly.id
    }
    
    variables = RequestContext(request, data)
    return render_to_response("usecase/inner_c_uc5.3.html", variables)
    
    
'''
TemplateView class for consumer use case 3.2
'''                                                                  
class c_uc32(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        #donutchart=[{"label":"You"   , "value":"", "color":"#80B1D3"},{"label":"Area" , "value":"", "color":"#C0C0C0"}]
        comparechart=[
            {
                "Units": "",
                "Data": _("Area")
            },
            {
                "Units": "",
                "Data": _("You")
            }
        ]
        compare = iutility.getPostValue("compare",request)
        year    = iutility.getPostValue("year",request)
        period  = iutility.getPostValue("period",request)        

        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id   

        d = idma() #class with dma related calcualtion
        
        #dma that will use for comparison
        dma  = household.dma  #get dma of the user
        #dma = DMA.objects.get(pk=11) #chosing other DMA for comparison, we will change this when we will get the different demographic database
        household_dma = dma.households.all()        
        
        #hourly series
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_monthly = series.readseries(ts_monthly)
        
        hhold = ihousehold()
        #print hhold.getseasonusage(user,year,compare)    
        '''
        We will only perform the following operation if the timeseries_hourly has sufficient data for analysis.
        If there is not sufficient data then simply return nothing and deal with client side. At the moment there
        is no check in the development environment as we know there are plenty of data for analysis
        '''
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
         #create pandas Series (time series using two different list for timeseries data analysis
        pdf = pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        data = {}

        if period=="season":
            data["you"]  = hhold.getseasonusage(user,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            data["area"] = d.getseasonusage(household_dma,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]                    
        elif period=="days": #if period is defined in range
            stdate       = iutility.getPostValue("stdate",request)
            endate       = iutility.getPostValue("endate",request)
            data["you"]  = hhold.getperiodstats(user,stdate,endate)
            data["area"] = d.getperiodstats(household_dma,stdate,endate)
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]                                
        else:
            data["you"]  = hhold.getmonthlyusage(user,int(period))
            data["area"] = d.getmonthlyusage(household_dma,int(period))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]   
        '''
        if period=="days": #if period is defined in range
            stdate       = iutility.getPostValue("stdate",request)
            endate       = iutility.getPostValue("endate",request)
            if compare=="night":
                data["you"]  = hhold.getnightstats(user,period=period,stdate=stdate,endate=endate)
                data["area"] = d.getnightstats(household_dma,period=period,stdate=stdate,endate=endate)
            else:
                data["you"]  = hhold.getdaystats(user,period=period,stdate=stdate,endate=endate)
                data["area"] = d.getdaystats(household_dma,period=period,stdate=stdate,endate=endate)            
        else:  
            if compare=="summer": #summer
                data["you"]  = hhold.getsummerstats(user,year)   #you
                data["area"] = d.getsummerstats(household_dma,year) #area
            
            elif compare=="winter": #winter ststictics comparison
                data["you"]  = hhold.getwinterstats(user,year)   #you
                data["area"] = d.getwinterstats(household_dma,year)
                      
            elif compare=="night": #night
                data["you"]  = hhold.getnightstats(user,int(period))   #you
                data["area"] = d.getnightstats(household_dma,int(period))
    
            elif compare=="day": #day
                data["you"]  = hhold.getdaystats(user,int(period))   #you
                data["area"] = d.getdaystats(household_dma,int(period))

        if data["you"]:
            dt = data["you"]
            a = dt[len(dt)-1]
            b = a["yourdata"]
            donutchart[0]["value"] = b["sum"]                        
            comparechart[1]["Units"] = b["sum"]
            
        if data["area"]:
            dt = data["area"]
            a = dt[len(dt)-1]
            b = a["areadata"]
            donutchart[1]["value"] = b["household"]
            #data["donutchart"] = donutchart 
            comparechart[0]["Units"] = b["household"]
                      
        '''            
        if not data["you"] or not data["area"]:
            data = None
        else:
            #data["donutchart"] = donutchart
            data["comparechart"] = comparechart
            data["title1"] = _("Total Units Consumed for household")
            data["title2"] = _("Units consumed per occupant")
            data["title3"] = _("Total Units Consumed for household")
            data["title4"] = _("Units consumed per occupant")
            data["area_label"] = _("Area")
            data["data_label"] = _("Data")
            data["you_label"] = _("You")
            data["units_label"] = _("Units")
            data["date_label"] = _("Date")

        #print data["comparechart"]            
        return HttpResponse(json.dumps(data),content_type='application/javascript')
    
'''
TemplateView class for consumer use case 3.3
'''
class c_uc33(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        donutchart=[
            {
                "label": "You",
                "value": "",
                "color": "#80B1D3"
            },
            {
                "label": "Area",
                "value": "",
                "color": "#C0C0C0"
            }
        ]
        comparechart = [
            {
                "Units": "",
                "Data": _("Area")
            },
            {
                "Units": "",
                "Data": _("You")
            }
        ]
        compare = iutility.getPostValue("compare",request)
        year    = iutility.getPostValue("year",request)
        period  = iutility.getPostValue("period",request)        
        #season  = iutility.getPostValue("season",request) 
        #season  = iutility.getPostValue("season",request)
        
        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id

        #dma that will use for comparison
        dma = DMA.objects.get(pk=2) #chosing other DMA for comparison, we will change this when we will get the different demographic database
                 
        #dma  = household.dma  #get dma of the user
        household_dma = dma.households.all()
        
        d = idma() #class with dma related calcualtion
            
        #dma that will use for comparison
        #dma = DMA.objects.get(pk=10) #chosing other DMA for comparison, we will change this when we will get the different demographic database
        #household_dma = dma.households.all()        
        
        #hourly series
        series     = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_monthly = series.readseries(ts_monthly)
                
        hhold = ihousehold()
        '''
        We will only perform the following operation if the timeseries_hourly has sufficient data for analysis.
        If there is not sufficient data then simply return nothing and deal with client side. At the moment there
        is no check in the development environment as we know there are plenty of data for analysis
        '''
        #get dates and values in a separate list
        dates, units = IT.izip(*timeseries_monthly) #much better for longer data, returning tuples
         #create pandas Series (time series using two different list for timeseries data analysis
        pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])                   
        pdf.index.name = "dates"
        data = {}
        
        if period=="season":
            data["you"]  = hhold.getseasonusage(user,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            data["area"] = d.getseasonusage(household_dma,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]                    
        elif period=="days": #if period is defined in range
            stdate       = iutility.getPostValue("stdate",request)
            endate       = iutility.getPostValue("endate",request)
            data["you"]  = hhold.getperiodstats(user,stdate,endate)
            data["area"] = d.getperiodstats(household_dma,stdate,endate)
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"] 
        else:
            data["you"]  = hhold.getmonthlyusage(user,int(period))
            data["area"] = d.getmonthlyusage(household_dma,int(period))
            if data["you"] and data["area"]:                        
                comparechart[1]["Units"] = data["you"]["yourdata"]["household"]                        
                comparechart[0]["Units"] = data["area"]["areadata"]["household"]             
            ""
        '''
            if compare=="night":
                data["you"]  = hhold.getnightstats(user,period=period,stdate=stdate,endate=endate)
                data["area"] = d.getnightstats(household_dma,period=period,stdate=stdate,endate=endate)
            else:
                data["you"]  = hhold.getdaystats(user,period=period,stdate=stdate,endate=endate)
                data["area"] = d.getdaystats(household_dma,period=period,stdate=stdate,endate=endate)             
        else:    
            if compare=="summer": #summer
                data["you"]  = hhold.getsummerstats(user,year)   #you
                data["area"] = d.getsummerstats(household_dma,year) #area
            
            elif compare=="winter": #winter ststictics comparison
                data["you"]  = hhold.getwinterstats(user,year)   #you
                data["area"] = d.getwinterstats(household_dma,year)
                      
            elif compare=="night": #night
                data["you"]  = hhold.getnightstats(user,int(period))   #you
                data["area"] = d.getnightstats(household_dma,int(period))
    
            elif compare=="day": #day
                data["you"]  = hhold.getdaystats(user,int(period))   #you
                data["area"] = d.getdaystats(household_dma,int(period))

                      
        if data["you"]:
            dt = data["you"]
            a = dt[len(dt)-1]
            b = a["yourdata"]
            donutchart[0]["value"]   = data["you"]["seasondata"]["household"]                        
            comparechart[1]["Units"] = data["you"]["seasondata"]["household"]
            
        if data["area"]:
            dt = data["area"]
            a = dt[len(dt)-1]
            b = a["areadata"]
            donutchart[1]["value"] = b["household"]
            #data["donutchart"] = donutchart 
            comparechart[0]["Units"] = b["household"]
                         
        '''            
        if not data["you"] or not data["area"]:
            data = None
        else:
            #data["donutchart"] = donutchart
            data["comparechart"] = comparechart
            data["title1"] = _("Total Units Consumed for household")
            data["title2"] = _("Units consumed per occupant")
            data["title3"] = _("Total Units Consumed for household")
            data["title4"] = _("Units consumed per occupant")
            data["area_label"] = _("Area")
            data["data_label"] = _("Data")
            data["you_label"] = _("You")
            data["units_label"] = _("Units")
            data["date_label"] = _("Date")

                    
        return HttpResponse(json.dumps(data),content_type='application/javascript')
        
#TemplateView class for consumer dashboard                                                                  
class c_uc52(TemplateView):
    template_name = "dashboard.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self, request, *args, **kwargs):
        #declaration
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
        data = {}        

        #capture data
        period = iutility.getPostValue("period",request)                

        #extract timeseries data        
        user       = request.user
        household  = user.households.all()[0]
        hhold      = ihousehold()
        series     = iseries()
        
        #if period != "days":
        if period=="season": 
            data = hhold.getseasoncost(user,iutility.getPostValue("seasonyear",request),iutility.getPostValue("season",request))
        elif period=="days":
            '''
            range of dates for extracting timeseries data
            '''
            stdate = iutility.getPostValue("stdate",request)
            endate = iutility.getPostValue("endate",request)
            
            #number of months to process data
            period = iutility.diffmonth(iutility.getstrTodate(endate,"%Y-%m-%d"),iutility.getstrTodate(stdate,"%Y-%m-%d")) + 1
            
            '''
            obtain timeseries for specified date range
            '''
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
                        tariff1 = hhold.tariff1(float(units[x]))
                        tariff1data["sum"] = tariff1data["sum"] + tariff1
                        list1.append(round(tariff1,2))
                                     
                        tariff2 = hhold.tariff2(float(units[x]))
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
                    data["title"]   = _("TARIFF COMPARISON FROM ")+stdate+ _(" TO ") +endate
            else:
                data = None
        else:    
            period = int(period)
            ts_monthly = series.getseriesmonths(series.readseries(series.getmonthlyseries(household)),period) #get timeseries
            if ts_monthly: #data available for the specified period
                '''
                prepare data for processing
                '''
                #get dates and values in a separate list
                dates, units = IT.izip(*ts_monthly) #much better for longer data, returning tuples
                #create pandas Series (time series using two different list for timeseries data analysis
                pdf =  pd.DataFrame(list(units),index=list(dates),columns=["units"])    #dateframe unused          
                pdf.index.name = "dates"               
                    
                '''
                prepare data to be used in client (browser)
                Note: This code can be optimised if processed using panda dataframe. To do this ihousehold class tariff1 and tariff2 needs to be rewrite using panda dataframe
                '''             
                for x in range(0, period):
                    dtlist.append(str(dates[x].date()))
                    
                    tariff1 = hhold.tariff1(units[x])
                    tariff1data["sum"] = tariff1data["sum"] + tariff1
                    list1.append(round(tariff1,2))
    
                    tariff2 = hhold.tariff2(units[x])
                    tariff2data["sum"] = tariff2data["sum"] + tariff2
                    list2.append(round(tariff2,2))
                
                tariff1data["sum"]      = round(tariff1data["sum"],2)                                            
                tariff1data["avg"]      = round(tariff1data["sum"]/period,2)
                tariff1data["high"]     = {"date":iutility.convertdate(dtlist[list1.index(max(list1))],'%Y-%m-%d','%B-%Y'),"max":max(list1)} #max per nonth
                tariff1data["low"]      = {"date":iutility.convertdate(dtlist[list1.index(min(list1))],'%Y-%m-%d','%B-%Y'),"min":min(list1)} #min per nonth
                
                tariff2data["sum"]      = round(tariff2data["sum"],2)                                  
                tariff2data["avg"]      = round(tariff2data["sum"]/period,2)
                tariff2data["high"]     = {"date":iutility.convertdate(dtlist[list2.index(max(list2))],'%Y-%m-%d','%B-%Y'),"max":max(list2)} #max per nonth
                tariff2data["low"]      = {"date":iutility.convertdate(dtlist[list2.index(min(list2))],'%Y-%m-%d','%B-%Y'),"min":min(list2)} #min per nonth
                                
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
                data["title"]   = _("TARIFF COMPARISON FOR THE LAST ") +str(period)+ _(" MONTHS")
            else:
                data = None
  
            
        return HttpResponse(json.dumps(data),content_type='application/javascript')

    
#TemplateView class for consumer dashboard                                                                  
class getcompare(TemplateView):
    template_name = "dashboard.html"
    
    def post(self, request, *args, **kwargs):
        #get form values
        comp = iutility.getPostValue("compare",request)
        occu = iutility.getPostValue("occupants",request)
        prop = iutility.getPostValue("property",request)
            
        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id      
        dma  = household.dma  #get dma of the user
                
        #monthly series
        series = iseries()
        ts_monthly = series.getmonthlyseries(household)
        timeseries_month = series.readseries(ts_monthly)
        length = len(timeseries_month)
            
        obj = {}
        data= []

        if comp=="high" or comp=="low" or comp=="avg":
            if occu and prop:
                dmastats = userDMAstats.objects.filter(household=household,options=3)                
            if occu and not prop:
                dmastats = userDMAstats.objects.filter(household=household,options=1)
            elif not occu and prop:
                dmastats = userDMAstats.objects.filter(household=household,options=2)
            else:
                dmastats = DMAstats.objects.filter(dma__pk=dma.pk)

                                                  
        #dmastats = DMAstats.objects.filter(dma__pk=dma.pk)
        if not dmastats:
            data = False
        
        ##getting DMA status for highest consumer      
        if comp=="high" and dmastats:
            for st in dmastats:
                obj["Units"] = str(st.maxunits)
                obj["Cost"]  = str(series.getCost(st.maxunits))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "Consumer"
                data.append(obj)
                obj = {}
                
                tseries      = timeseries_month[length-st.statsperiod:]
                obj["Units"] = str(series.getSum(tseries))
                obj["Cost"]  = str(series.getCost(float(obj["Units"])))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "You"
                data.append(obj)
                obj = {}

            #running in a seprate loop so it will be easy to separate on the client side
            for st in dmastats:
                obj["period"]    = st.statsperiod
                obj["household"] = st.sumhouseholds
                obj["occupant"]  = st.sumoccupants
                obj["average"]   = st.sumoccupants/st.sumhouseholds
                data.append(obj)
                obj = {}  
                                
            obj["title"] = _("Your last 12 Months bill comparison vs highest consumers")
            data.append(obj)                
            
        ##getting DMA status for lowest consumer
        elif comp=="low" and dmastats:
            for st in dmastats:
                obj["Units"] = str(st.minunits)
                obj["Cost"]  = str(series.getCost(st.minunits))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "Consumer"
                data.append(obj)
                obj = {}
                tseries      = timeseries_month[length-st.statsperiod:]
                obj["Units"] = str(series.getSum(tseries))
                obj["Cost"]  = str(series.getCost(float(obj["Units"])))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "You"
                data.append(obj)
                obj = {}

            #running in a seprate loop so it will be easy to separate on the client side
            for st in dmastats:
                obj["period"]    = st.statsperiod
                obj["household"] = st.sumhouseholds
                obj["occupant"]  = st.sumoccupants
                obj["average"]   = st.sumoccupants/st.sumhouseholds
                data.append(obj)
                obj = {}  
                                
            obj["title"] = _("Your last 12 Months bill comparison vs lowest consumers")
            data.append(obj)
            
        elif comp=="avg" and dmastats:
            #getting DMA status for the average unit/bill            
            for st in dmastats:
                obj["Units"] = str(st.avgunits)
                obj["Cost"]  = str(series.getCost(st.avgunits))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "DMA"
                data.append(obj)
                obj = {}
                tseries      = timeseries_month[length-st.statsperiod:]
                obj["Units"] = str(series.getSum(tseries))
                obj["Cost"]  = str(series.getCost(float(obj["Units"])))
                obj["Period"]= str(st.statsperiod)+" Month"
                obj["Data"]  = "You"
                data.append(obj)
                obj = {}
            
            #running in a seprate loop so it will be easy to separate on the client side
            for st in dmastats:
                obj["period"]    = st.statsperiod
                obj["household"] = st.sumhouseholds
                obj["occupant"]  = st.sumoccupants
                obj["average"]   = st.sumoccupants/st.sumhouseholds
                data.append(obj)
                obj = {}                
                                
            obj["title"] = _("Your last 12 Months bill comparison vs other consumers")
            data.append(obj)
                
        return HttpResponse(json.dumps(data),content_type='application/javascript')
        
#View class for detecting user type and redirect to relevant TemplateView
class dashboard(View):
    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff): #if not a super user or staff
            view = consumer.as_view() #return consumer
            return view(request, *args, **kwargs)
        else:
            try:
                hid = self.kwargs['household_id']   #check for household if in case superuser
            except:
                hid = None
                
            if not hid:     #if there is no household id
                view = superuser.as_view()  #return to superuser view
            else:
                view = consumer.as_view()   #else return consumer view and process household_id inside that view
                
            return view(request, *args, **kwargs)      

#TemplateView class for agent based modelling page only available to superuser        
class policy(TemplateView):
    template_name = "policy.html"
        
    def get(self,request,**kwargs):
        return self.render_to_response({}) 

#TemplateView class to show DMAs to superuser
class dmas(TemplateView):
    template_name = "dmas.html"
    
    def get(self,request,**kwargs):
        from iwidget.views import dmas_view
        values = dmas_view(request,self.kwargs['dma_id'])
        data = {
            'dma': values["dma"],
            'charts': values["charts"],
            'js_data': values["js_data"]
        }
        return self.render_to_response(data)  

#TemplateView to show timeseries that ope in new window
class timeseries(TemplateView):
    template_name = "timeseries.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def get(self,request,**kwargs):
        object_id = self.kwargs['object_id']
        user = request.user
        try:
            ts = IWTimeseries.objects.get(pk=object_id)
        except IWTimeseries.DoesNotExist:
            raise Http404('Timeseries object does not exist')
        is_household = hasattr(ts.gentity, 'gpoint') and hasattr(ts.gentity.gpoint,
                'household')
        if not (user.is_staff or user.is_superuser) and \
                (not is_household or ts.gentity.gpoint.household.user.id != user.id):
            request.notifications.error("Permission denied")
            return HttpResponseRedirect(reverse('index'))
        '''  
        context['related_station'] = self.object.related_station
        context['enabled_user_content'] = settings.ENHYDRIS_USERS_CAN_ADD_CONTENT
        context['display_copyright'] = settings.ENHYDRIS_DISPLAY_COPYRIGHT_INFO
        context['anonymous_can_download_data'] = \
            settings.ENHYDRIS_TSDATA_AVAILABLE_FOR_ANONYMOUS_USERS
        return context
        '''
                  
        return self.render_to_response({"timeseries":ts})    
'''
This class deals with the consumer use case 5.3 which is to do with bill forecasting.
It is dependent on the Forecast model and Iforecast class and JAVA based Weka machine learning and data mining libray
The bridge between JAVA and python is made using py4j which connect python through to Java by connect through JVM port
'''
class c_uc53(TemplateView):
    template_name = "index.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self,request):
        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id
        #series = iseries()
        #ts_monthly = series.getmonthlyseries(household)
        #timeseries_month = series.readseries(ts_monthly)
        data = ""        
        dailyfile = ""
        yearfile = ""
        type   = request.POST.get("algo")
        period = request.POST.get("period")
        series = iseries()
        gateway = JavaGateway() 
        entry = gateway.entry_point #connect to JVM
        javats = entry.getTimeSeries(str(user.id)) #get this user javatimeseries object
        ifcast = iforecast(javats)        
        
        forecast = Forecast.objects.get(user__pk=user.pk)
        if period=="days": #daily forecast
            ts_daily = series.getdailyseries(household)
            timeseries_daily = series.readseries(ts_daily)
            if forecast.dailyfile and len(timeseries_daily)>60: #forecast only when data has 60 days historical cost or usage
                dailyfile = forecast.dailyfile
            else:
                return HttpResponse(json.dumps(False),content_type='application/javascript')
        else: #yearly fordcast
            ts_monthly = series.getmonthlyseries(household)
            timeseries_month = series.readseries(ts_monthly)
            if forecast.yearfile and len(timeseries_month)>12: #forecast only when data has 12 months of historical cost or usage. later can be fixed for other intervals
                yearfile = forecast.yearfile
            else:
                return HttpResponse(json.dumps(False),content_type='application/javascript')                                                  
  
        if period=="quarter":    
            data = ifcast.getForecast(timeseries_month,3,type,yearfile)
            '''
            sum = ifcast.getCost(ifcast.getSum(data))
            high= ifcast.getHighestCost(data)
            low = ifcast.getLowestCost(data)
            avg = ifcast.getCost(ifcast.getAvg(data,3))
            data.append({"low":low})
            data.append({"high":high})
            data.append({"sum":sum}) 
            data.append({"avg":avg})
            data.append({"title":"NEXT 3 MONTHS BILL FORECAST"})
            '''
        elif period=="half":
            data = ifcast.getForecast(timeseries_month,6,type,yearfile)
            '''
            sum = ifcast.getCost(ifcast.getSum(data))
            high= ifcast.getHighestCost(data)
            low = ifcast.getLowestCost(data)
            avg = ifcast.getCost(ifcast.getAvg(data,6))
            data.append({"low":low})
            data.append({"high":high})
            data.append({"sum":sum}) 
            data.append({"avg":avg})
            data.append({"title":"NEXT 6 MONTHS BILL FORECAST"})
            '''        
        elif period=="year":
            data = ifcast.getForecast(timeseries_month,12,type,yearfile)
            '''
            sum = ifcast.getCost(ifcast.getSum(data))
            high= ifcast.getHighestCost(data)
            low = ifcast.getLowestCost(data)
            avg = ifcast.getCost(ifcast.getAvg(data,12))
            data.append({"low":low})
            data.append({"high":high})
            data.append({"sum":sum})
            data.append({"avg":avg})
            data.append({"title":"NEXT 12 MONTHS BILL FORECAST"})
            '''
        else:
            #print timeseries_daily, it is very slow and therefore not included, however it perfectly works, its browser display still needed fixing as 
            #chart will be displayed in days rather than months
            data = ifcast.getForecast(timeseries_daily,30,type,dailyfile,"days")
            '''
            sum = ifcast.getCost(ifcast.getSum(data))
            high= ifcast.getHighestCost(data)
            low = ifcast.getLowestCost(data)
            avg = ifcast.getCost(ifcast.getAvg(data,30))
            data.append({"low":low})
            data.append({"high":high})
            data.append({"sum":sum})
            data.append({"avg":avg})
            data.append({"title":"Next 30 days forecast"});
            '''
        return HttpResponse(json.dumps(data),content_type='application/javascript')                          

'''
This class deals with the consumer use case 5.4 which forecast the energyu bill associated with water consumption.
It is dependent on the Forecast model and Iforecast class and JAVA based Weka machine learning and data mining libray
The bridge between JAVA and python is made using py4j which connect python through to Java by connect through JVM port
'''
class c_uc54(TemplateView):
    template_name = "index.html"

    #@cache_page(30 * 60)  # cache for 30 minutes
    def post(self,request):
        user = request.user #get authenticated user
        household = user.households.all()[0] #get user household id
        data = ""        
        yearfile = ""
        type   = request.POST.get("algo")
        period = request.POST.get("period")
        series = iseries()
        gateway = JavaGateway() 
        entry = gateway.entry_point #connect to JVM
        javats = entry.getTimeSeries(str(user.id)) #get this user javatimeseries object

        #javats.safeThread();
        #entry.shutGateway()        
        ifcast = iforecast(javats)        
        
        forecast = ElectricForecast.objects.get(user__pk=user.pk)
        ts_monthly = series.getmonthlyseries(household)
        timeseries_month = series.readseries(ts_monthly)
        
        if forecast.yearfile and len(timeseries_month)>12: #forecast only when data has 12 months of historical cost or usage. later can be fixed for other intervals
            yearfile = forecast.yearfile
        else:
            return HttpResponse(json.dumps(False),content_type='application/javascript')                                                  
  
        data = ifcast.getForecast(timeseries_month,int(period),type,yearfile)
        
        '''
        if period=="quarter":    
            data = ifcast.getForecast(timeseries_month,3,type,yearfile)
        elif period=="half":
            data = ifcast.getForecast(timeseries_month,6,type,yearfile)
        elif period=="year":
            data = ifcast.getForecast(timeseries_month,12,type,yearfile)
        '''
            
        return HttpResponse(json.dumps(data),content_type='application/javascript')