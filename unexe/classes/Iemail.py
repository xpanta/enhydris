'''
Created on 10 Aug 2014
@author: adeel
'''

import smtplib
import sys
from email.MIMEText import MIMEText
from Iconfig import iconfig
 
'''
This is the class for sending email to users
'''
class iemail():
    def __init__(self,destination,subject,content):
        self.SMTPserver  = iconfig.SMTPServer
        self.sender      = iconfig.EmailSender                
        self.username    = iconfig.SMTPUsername
        self.password    = iconfig.SMTPPassword
        self.port        = iconfig.SMTPPort
        self.destination = destination     
        self.subject     = subject   
        self.content     = content
        self.txt_subtype = 'plain'
    
    def setContent(self,content):
        self.content = content
    
    def setDestination(self,destination):
        self.destination = destination

    def setSubject(self,subject):
        self.subject = subject
        
    def sendEmail(self):
        try:
            #compose message
            msg = MIMEText(self.content, self.txt_subtype)
            msg['Subject']= self.subject
            msg['From']   = self.sender # some SMTP servers will do this automatically, not all
            
            #connect and handshake
            conn = smtplib.SMTP(self.SMTPserver,self.port)
            conn.ehlo()
            conn.starttls()
            conn.ehlo()
            #conn.set_debuglevel(False)
            #login
            conn.login(self.username, self.password)            
            try:
                conn.sendmail(self.sender, self.destination, msg.as_string())
                print "Email sent..."  
            finally:
                conn.close()
                
        except Exception, exc:
            sys.exit( "mail failed; %s" % str(exc) ) # give a error message
                
        return    
    