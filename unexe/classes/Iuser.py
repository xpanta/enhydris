'''
Created on 06 Mar 2014
@author: adeel
'''
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from Iserialize import iserialize
from Iutility import iutility
import time
'''
This is the user class and all functionality related to user are implemeted in this class.
Some of these include login, logout etc
'''
class iuser():    
    def __init__(self):
        #column of the user class
        self.col = ['first_name','last_name','email']
        
    '''
    This method retrives user from database and serialize it
    Still this needs to be dumps before sending to client
    '''
    def getuser(self,loggeduser):
        try:
            loggeduser = User.objects.filter(pk=loggeduser.pk)
            serialize  = iserialize()
            return serialize.modelToJSON(loggeduser,self.col)            
        except:
            return -1 #indcates other issues or errors, it needs to be redirected to universal error
    
    '''
    This method authenticate user and create user session
    uname:   username
    passwd:  user password
    request: HTTP request object
    return:  False - indicating username and password is incorrect
    return:  0 - when account is disabled
    return:  True - when successfully logged in 
    '''    
    def login(self,uname,passwd,request):
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                #User is valid, active and authenticated
                auth_login(request,user)
                return True
            else:
                #The password is valid, but the account has been disabled!
                return 0
        else:
            # the authentication system was unable to verify the username and password
            #The username and password were incorrect
            return False
        
    '''
    This method change user password
    ***please make sure don't pass the null or empty string or other garbage value***
    loggeduser: is authenticated user object
    oldpasswd:  current user password
    newpasswd:  new password
    return   :  True  - when password change successfully.
    return   :  False - when old password is incorrect
    return   :  -1 - exception occurred indicating null object
    '''
    def changepassword(self,loggeduser,oldpasswd, newpasswd):
        try:
            if loggeduser.check_password(oldpasswd) is True:
                loggeduser.set_password(newpasswd)
                loggeduser.save()
                return True #password change successfully
            else:
                return False    #old password is incorrect
        except:
            return -1 #indcates other issues or errors, it needs to be redirected to universal error
      
    '''      
    Update user details
    ***please make sure don't pass the null or empty string or other garbage value***
    loggeduser: is authenticated user object
    values    : is a dictionary of values. It must be the combination of {database column:database value}
    return    : True - Indicate user details change successfully
    return    : -1 - indicate exception or undefined error
    '''
    def updateuser(self,loggeduser,values):
        try:
            del values['csrfmiddlewaretoken'] #make sure to get rid of any csrfmiddlewaretoken before comitting saving to db 
        except:
            pass
        
        try:
            User.objects.filter(pk=loggeduser.pk).update(**values)
            return True #user details save successfully
        except:
            return -1 #indcates other issues or errors, it needs to be redirected to universal error
    
    '''
    This method is used to create username which is complaint with Django username field in user table
    #str: This is any random string. First 3 characters are used for generating username (3 characters+timestamp)
        >>> Iuser.getUsername(ahs1d)
        >>> ahs2124654654
    '''
    def getUsername(self,astring):
        name = iutility.getAlphanumeric(astring)
        if len(name)>2:
            return name[0:3]+str(int(time.time())) #get first 3 charaters of email and add timestamp to create unique username
        else:
            return name+str(int(time.time()))

    '''
    This method is used to create password using asicii chacters and digits
    #size: This is the size of the required password - default is 8 characters
        >>> Iuser.getPassword(8)
        >>> ABD2JX98
    '''
    def getPassword(self,size=8):
        return iutility.getRandomstring(size)