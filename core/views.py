from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login
#!TODO import ugetext for internationalizing texts
from django.contrib.auth.models import User

from iwidget.models import UserValidationKey, Household


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
        username = request.POST.get("username", None)
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

            try:
                User.objects.get(username=username)
                user_found = True
            except User.DoesNotExist:
                user_found = False
            if nocc:
                if is_email(email):
                    if not user_found:
                        if pwd1 == pwd2:
                            user.username = username
                            user.first_name = first
                            user.last_name = last
                            user.email = email
                            user.set_password(pwd1)
                            user.save()
                            profile = user.get_profile()
                            profile.fname = first
                            profile.lname = last
                            profile.address = ", ".join([addr, postal])
                            profile.save()
                            household.num_of_occupants = nocc
                            household.address = ", ".join([addr, postal])
                            household.save()
                            uvk.used = True
                            uvk.save()
                            messages.add_message(request,
                                                 messages.INFO,
                                                 "Thank you! You may now login "
                                                 "with your "
                                                 "chosen username and password!")
                            return HttpResponseRedirect("/login")
                        else:
                            messages.add_message(request,
                                                 messages.ERROR,
                                                 "Passwords do not match")
                    else:
                        messages.add_message(request,
                                             messages.ERROR,
                                             "Username is taken. "
                                             "Please choose another one.")
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
            'username': username,
            'address': addr,
            'postal': postal,
            'email': email,
        }
        variables = RequestContext(request, data)
        return render_to_response("validate.html", variables)


