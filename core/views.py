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
    if request.method == "GET":
        data = {}
        variables = RequestContext(request, data)
        return render_to_response("signup.html", variables)
    elif request.method == "POST":
        mid = request.POST.get("mid", None)
        key = request.POST.get("key", None)
        if mid and key:
            try:
                user = User.objects.get(username=mid)
                UserValidationKey.objects.get(user=user,
                                              key=key, used=False)
                # we can't revers with args and kwargs. Maybe in the future
                return HttpResponseRedirect("/core/user/profile/{x}/"
                                            "?m={m}&k={k}"
                                            .format(x=user.id, m=mid, k=key))
            except (User.DoesNotExist, UserValidationKey.DoesNotExist):
                messages.add_message(request, messages.INFO,
                                     'Meter id or password are not valid. '
                                     'Please try again! or contact the '
                                     'system administrator')
                return HttpResponseRedirect(reverse("signup"))


def user_profile(request, uid):

    def is_email(text):
        import re
        pattern = '[\.\w]{1,}[@]\w+[.]\w+'
        if re.match(pattern, text):
            return True
        else:
            return False

    if request.method == "GET":
        user = User.objects.get(pk=uid)
        household = user.households.all()[0]  # get user household id
        try:
            uvk1 = UserValidationKey.objects.get(user=user)
            mid = request.GET.get("m", "")
            key = request.GET.get("k", "")
            mid = mid[2:]
            uvk2 = UserValidationKey.objects.get(identifier=mid, key=key,
                                                 used=False)
            if uvk1 == uvk2:  # for security purposes, we check values.
                meter_id = uvk1.identifier
                data = {
                    "household": household,
                    "nocc": '1',
                    "mid": meter_id,
                    "key": key,
                    "profile": user.get_profile(),
                    "user_id": user.id,
                }
                variables = RequestContext(request, data)
                return render_to_response("user_form.html", variables)
        except UserValidationKey.DoesNotExist:
            messages.add_message(request, messages.INFO, "Meter id and Keypass "
                                                         "combination is "
                                                         "not valid!")
            return HttpResponseRedirect(reverse("signup"))
    elif request.method == "POST":
        first = request.POST.get("first", None)
        last = request.POST.get("last", None)
        email = request.POST.get("email", None)
        username = request.POST.get("username", None)
        pwd1 = request.POST.get("passwd1", None)
        pwd2 = request.POST.get("passwd2", None)
        addr = request.POST.get("addr", "")
        postal = request.POST.get("postal", "")
        mid = request.POST.get("mid")
        key = request.POST.get("key")
        uid = request.POST.get("uid")
        try:
            User.objects.get(username=username)
            found = True
        except User.DoesNotExist:
            found = False
        if not found:
            try:
                user = User.objects.get(pk=uid)
                household = user.households.all()[0]  # get user household id
            except (User.DoesNotExist, Household.DoesNotExist):
                raise Http404("User not found!")
            try:
                nocc = int(request.POST.get("nocc", 1))
            except (ValueError, KeyError):
                nocc = 1
            if is_email(email):
                if pwd1 == pwd2:
                    uvk = UserValidationKey.objects.get(mid=mid, key=key,
                                                        used=False)
                    if user == uvk.user:
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
                        return HttpResponseRedirect("/core/user/profile/{x}/"
                                                    "?m={m}&k={k}"
                                                    .format(x=uid, m=mid, k=key))
                    else:
                        messages.add_message(request,
                                             messages.ERROR,
                                             "Authentication Error. "
                                             "Please contact the System "
                                             "Administrator for this issue!")
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
                                 "Username name is already taken. "
                                 "Please choose another!")
        data = {
            "household": household,
            "nocc": nocc,
            "mid": mid,
            "key": key,
            "user_id": user.id,
            'first': first,
            'last': last,
            'username': username,
            'address': addr,
            'postal': postal,
            'email': email,
        }
        variables = RequestContext(request, data)
        return render_to_response("user_form.html", variables)
