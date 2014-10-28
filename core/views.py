from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
#!TODO import ugetext for internationalizing texts
from django.contrib.auth.models import User
import logging
from iwidget.models import UserValidationKey, Household
import requests
from xml.dom import minidom
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
import os
import binascii
from sso.common import encrypt_and_hash_pwd


def sso_redirect(request):
    xml = """
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <Decrypt xmlns="https://services.up-ltd.co.uk/cryptoservice_iwidget/">
              <CipherText>##TOKEN##</CipherText>
              <ServiceAccountName>IWidgetService</ServiceAccountName>
              <ServiceAccountPassword>1-Widg3t##Crypt0Service</ServiceAccountPassword>
            </Decrypt>
          </soap:Body>
        </soap:Envelope>
    """
    token = request.GET.get('t')
    log = logging.getLogger(__name__)
    if token:
        #http://iwidget.up-ltd.co.uk/core/sso/auth/?t=8A-6B-80-B7-D8-87-CC-EE-2D-58-1B-72-08-F6-7F-20-BC-FB-CE-5D-C8-6B-76-43-F0-C1-8A-15-15-68-85-7C-1E-98-7D-E2-F7-D4-AF-61-ED-62-D3-3C-F6-67-8B-10-DE-7C-73-48-74-65-34-F8-A4-B2-65-1A-B9-9E-32-FE
        #superuser token:
        #http://localhost:8000/core/sso/auth/?t=94-66-FC-83-3F-28-95-F6-06-E2-A6-BA-85-57-B0-D4-7E-F6-C6-D7-CF-28-7B-17-20-B6-5A-9F-6E-98-18-87-10-8A-2A-C7-F7-2C-17-9C-51-C9-DD-41-0F-FA-92-10-01-53-5B-FA-0C-50-F2-E9-E4-71-A6-A3-25-EB-B7-BC
        # empty as of 23/10 user 059E14?
        #http://localhost:8000/core/sso/auth/?t=44-28-E7-A5-4B-ED-D8-1E-8B-95-4C-E9-9E-05-79-FA-79-82-15-63-3C-D4-DA-71-92-52-8C-AD-A4-18-76-25-B7-15-26-66-20-DE-9C-9E-52-A4-03-2A-3F-3C-D3-D7-5B-01-01-A1-18-CE-27-3A-93-5B-2B-89-71-77-FB-3E
        # 006063
        #http://localhost:8000/core/sso/auth/?t=BC-7A-AF-90-AC-D6-60-18-35-BD-A2-96-AB-6A-18-B1-8C-F4-65-21-50-F6-6A-CF-7D-1F-59-DF-8C-0E-5F-2F-C0-67-45-A7-59-A9-36-9A-46-58-7D-29-FA-92-57-6E-40-90-86-B6-34-2E-A9-21-9B-B7-38-14-68-EC-14-1A
        #log.debug("Received token %s" % token)
        # 0062702 (old - no energy)
        #http://localhost:8000/core/sso/auth/?t=C8-2A-CD-F8-A3-5D-02-6F-B0-3E-1C-78-05-52-76-83-88-8E-BC-E7-8E-78-C0-36-A5-1E-0A-7C-F1-A5-11-C5-79-2A-66-04-E2-A2-91-55-4D-F5-E5-BA-26-7B-6D-11-D1-E6-34-A1-AB-4D-2F-1A-F4-27-61-B6-43-AA-34-F7
        xml = xml.strip()
        xml = xml.replace("##TOKEN##", token)
        url = "https://services.up-ltd.co.uk/cryptoservice_iwidget/service.asmx"
        headers = {'Content-Type': 'text/xml'}
        res = requests.post(url, data=xml, headers=headers)
        log.debug("received token %s" % token)
        if res.status_code == requests.codes.ok:
            doc = minidom.parseString(res.text)
            result = doc.getElementsByTagName("DecryptResult")[0]
            text = result.firstChild.data
            #log.debug("text is %s" % text)
            username = text.split("|")[0]
            username = username.replace('@', '')
            log.debug("username is %s" % username)
            user = User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            #user = authenticate(username=user.username, password=user.password)
            login(request, user)
            popup = False
            try:
                uvk = UserValidationKey.objects.get(user=user)
                popup = uvk.popup
            except UserValidationKey.DoesNotExist:
                pass
            if popup:
                return HttpResponseRedirect(reverse("user_profile"))
            else:
                return HttpResponseRedirect(reverse("dashboard"))
        else:
            logout(request)
            return HttpResponseRedirect(reverse("login"))
    else:
        logout(request)
        return HttpResponseRedirect(reverse("login"))


def reset_form(request):

    def is_email(text):
        import re
        pattern = '[\.\w]{1,}[@]\w+[.]\w+'
        if re.match(pattern, text):
            return True
        else:
            return False

    if request.method == "GET":
        data = {}
        variables = RequestContext(request, data)
        return render_to_response("reset_form.html", variables)
    elif request.method == "POST":
        email = request.POST.get("email", "")
        if is_email(email):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                key = str(binascii.hexlify(os.urandom(4)).upper())
                key = key.replace('E', 'B')
                key = key.replace('0', '1')
                if not key[0].isalpha():
                    key = "A" + key[:-1]
                xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><SetUserPassword xmlns="https://services.up-ltd.co.uk/adminservice_iwidget/"><name>##USER##</name><password>##PASSWORD##</password><serviceUsername>IWidgetService</serviceUsername><servicePassword>1-Widg3t##Crypt0Service</servicePassword></SetUserPassword></soap:Body></soap:Envelope>"""
                enc_pwd = encrypt_and_hash_pwd(key)
                xml = xml.replace("##USER##", user.username) \
                    .replace("##PASSWORD##", enc_pwd)
                headers = {'Content-Type': 'text/xml'}
                res = requests.post('https://services.up-ltd.co.uk/'
                                    'adminservice_iwidget/service.asmx',
                                    data=xml, headers=headers)
                status = False
                if res.status_code == requests.codes.ok:
                    doc = minidom.parseString(res.text)
                    result = doc.getElementsByTagName("SetUserPasswordResult")[0]
                    val = result.firstChild.data
                    if val == "true":  # True only if SSO update was OK!!
                        status = True
                        user.set_password(key)
                        try:
                            uvk = UserValidationKey. \
                                objects.get(user=user)
                            uvk.key = key
                            uvk.save()
                        except UserValidationKey.DoesNotExist:
                            uvk = UserValidationKey. \
                                objects.create(user=user,
                                               identifier="",
                                               key=key,
                                               sso=True,
                                               popup=False)
                if status:
                    subject = "iWIDGET: New Password Request!"
                    to = [user.email]
                    from_email = 'no-reply@iwidget.up-ltd.co.uk'
                    ctx = {
                        'username': user.username,
                        'pwd': key,
                    }
                    message = get_template('password.html')\
                        .render(Context(ctx))
                    msg = EmailMessage(subject, message, to=to,
                                       from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()
                    messages.add_message(request,
                                         messages.ERROR,
                                         "We have send you an email with your "
                                         "new password. Thank you!")
                    return HttpResponseRedirect(reverse("reset_form"))
                else:
                    messages.add_message(request,
                                         messages.ERROR,
                                         "There was a problem. Please, try "
                                         "again, later!")
                    return HttpResponseRedirect(reverse("reset_form"))
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "This email has not been registered! "
                                     "Please contact the system administrator "
                                     "if the issue persists.")
                return HttpResponseRedirect(reverse("reset_form"))
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Please, provide a valid email address")
            return HttpResponseRedirect(reverse("reset_form"))


def user_profile(request):

    def is_email(text):
        import re
        pattern = '[\.\w]{1,}[@]\w+[.]\w+'
        if re.match(pattern, text):
            return True
        else:
            return False

    user = request.user
    if request.method == "GET":
        data = {
            "user_id": user.id
        }
        variables = RequestContext(request, data)
        return render_to_response("user_profile.html", variables)
    elif request.method == "POST":
        user_id = request.POST.get("t", "0")
        user_id = int(user_id)
        user = request.user
        if user.id == user_id:
            first = request.POST.get("first", "")
            last = request.POST.get("last", "")
            email = request.POST.get("email", "")
            nocc = request.POST.get("nocc", "")
            email_valid = is_email(email)
            try:
                nocc = int(nocc)
            except ValueError:
                nocc = 0
            if email_valid:
                if nocc:
                    profile = user.get_profile()
                    profile.fname = first
                    profile.lname = last
                    profile.save()
                    user.first_name = first
                    user.last_name = last
                    user.email = email
                    user.save()
                    household = user.households.all()[0]
                    household.num_of_occupants = nocc
                    household.save()
                    try:
                        uvk = UserValidationKey.objects.get(user=user)
                        uvk.popup = False
                        uvk.save()
                    except UserValidationKey.DoesNotExist:
                        pass
                    return HttpResponseRedirect(reverse("dashboard"))
                else:
                    messages.add_message(request,
                                         messages.ERROR,
                                         "Please, provide the number of "
                                         "occupants in your house")
                    return HttpResponseRedirect(reverse("user_profile"))
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Please, provide a valid email "
                                     "address")
                return HttpResponseRedirect(reverse("user_profile"))
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "User is not authenticated!")
            return HttpResponseRedirect(reverse("user_profile"))
    else:
        return HttpResponseRedirect(reverse("user_profile"))


def signup(request):

    def is_email(text):
        import re
        pattern = '[\.\w]{1,}[@]\w+[.]\w+'
        if re.match(pattern, text):
            return True
        else:
            return False

    if request.method == "GET":
        data = {}
        variables = RequestContext(request, data)
        return render_to_response("validate.html", variables)
    elif request.method == "POST":
        first = request.POST.get("first", None)
        last = request.POST.get("last", None)
        email = request.POST.get("email", None)
        pwd1 = request.POST.get("passwd1", None)
        pwd2 = request.POST.get("passwd2", None)
        addr = request.POST.get("addr", "")
        postal = request.POST.get("postal", "")
        key = request.POST.get("key")
        household = None
        nocc = 1
        try:
            uvk = UserValidationKey.objects.get(key=key, used=False)
            uvk_found = True
        except (User.DoesNotExist, UserValidationKey.DoesNotExist):
            uvk_found = False

        if uvk_found:
            try:
                user = uvk.user
                household = user.households.all()[0]  # get user household id
            except Household.DoesNotExist:
                raise Http404("Household not found!")

            try:
                nocc = int(request.POST.get("nocc", "0"))
                nocc = int(nocc)
            except (ValueError, KeyError):
                nocc = 0

            if nocc:
                if is_email(email):
                    if pwd1 == pwd2:
                        user.first_name = first
                        user.last_name = last
                        user.email = email
                        user.set_password(pwd1)
                        user.save()
                        profile = user.get_profile()
                        profile.fname = first
                        profile.lname = last
                        profile.address = " ".join([addr, postal])
                        profile.save()
                        household.num_of_occupants = nocc
                        household.address = " ".join([addr, postal])
                        household.save()
                        uvk.used = True
                        uvk.save()
                        messages.add_message(request,
                                             messages.INFO,
                                             "Thank you! You may now login "
                                             "with your "
                                             "username (%s) and "
                                             "password!" % user.username)
                        return HttpResponseRedirect("/login?u=" + user.username)
                    else:
                        messages.add_message(request,
                                             messages.ERROR,
                                             "Passwords do not match")
                else:
                    messages.add_message(request,
                                         messages.ERROR,
                                         "Please, provide a proper email address")
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Please, provide the number of occupants in your house")
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "This validation key does not exist. Please, "
                                 "try again!")

        data = {
            "household": household,
            "nocc": nocc,
            "key": key,
            'first': first,
            'last': last,
            'address': addr,
            'postal': postal,
            'email': email,
        }
        variables = RequestContext(request, data)
        return render_to_response("validate.html", variables)


