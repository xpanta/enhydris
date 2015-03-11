from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
from django.views.decorators.csrf import csrf_exempt
from iwidget.models import (UserValidationKey, Household,
                            UsageData, UserPageView)
import requests
from xml.dom import minidom
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
import os
import binascii
from sso.common import encrypt_and_hash_pwd
from datetime import datetime
from django.utils import translation


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
            if 'PT' in username:
                user_language = 'pt'
            elif 'GR' in username:
                user_language = 'el'
            else:
                user_language = 'en'
            translation.activate(user_language)
            request.LANGUAGE_CODE = translation.get_language()
            request.session['django_language'] = user_language
            # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
            log.debug("username is %s" % username)
            user = User.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            #user = authenticate(username=user.username, password=user.password)
            login(request, user)
            UsageData.objects.create(user=user)
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


@csrf_exempt
def user_exits(request):
    if request.method == "POST":
        username = request.POST.get('user', None)
        if username:
            user = User.objects.get(username=username)
            ud = UsageData.objects.filter(user=user).order_by('-enter_ts')[0]
            now = datetime.now()
            ud.exit_ts = now
            ud.save()
            return HttpResponse("OK")
        else:
            raise Http404("not a valid user")
    else:
        raise Http404("not a valid method")


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
                    subject = _("iWIDGET: New Password Request!")
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
                                         _("We have send you an email with your "
                                           "new password. Thank you!"))
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
                                     _("This email has not been registered! "
                                       "Please contact the system administrator "
                                       "if the issue persists."))
                return HttpResponseRedirect(reverse("reset_form"))
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 _("Please, provide a valid email address"))
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
                                         _("Please, provide the number of "
                                           "occupants in your house"))
                    return HttpResponseRedirect(reverse("user_profile"))
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     _("Please, provide a valid email "
                                       "address"))
                return HttpResponseRedirect(reverse("user_profile"))
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 _("User is not authenticated!"))
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
                                             _("Thank you! You may now login "
                                               "with your "
                                               "username (%s) and "
                                               "password!" % user.username))
                        return HttpResponseRedirect("/login?u=" + user.username)
                    else:
                        messages.add_message(request,
                                             messages.ERROR,
                                             _("Passwords do not match"))
                else:
                    messages.add_message(request,
                                         messages.ERROR,
                                         _("Please, provide a proper email address"))
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     _("Please, provide the number of occupants in your house"))
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


@csrf_exempt
def add_page_view(request):
    if request.method == "POST":
        username = request.POST.get('user', None)
        page_title = request.POST.get('page', None)
        if username:
            user = User.objects.get(username=username)
            ud = UserPageView.objects.create(
                user=user,
                page=page_title
            )
            ud.save()
            return HttpResponse("OK")
        else:
            raise Http404("not a valid user")
    else:
        raise Http404("not a valid method")

