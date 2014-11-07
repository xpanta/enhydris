from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from iwidget.models import UserNotifications
#!TODO import ugetext for internationalizing texts


@login_required
def user_events(request, username):
    f = request.GET.get("f", "all")
    _id = request.GET.get("hide", "")
    if _id:
        try:
            event = UserNotifications.objects.get(pk=_id)
            event.read = True
            event.save()
        except UserNotifications.DoesNotExist:
            pass
    if username == request.user.username:
        user = request.user
        notifications = UserNotifications.objects.filter(user=user)
        if f == "new":
            notifications = notifications.filter(read=False)
        elif f == "old":
            notifications = notifications.filter(read=True)
        notifications = notifications.order_by("-detected")
        data = {
            "events": notifications,
        }
        variables = RequestContext(request, data)
        return render_to_response("events_table.html", variables)
    else:
        raise Http404("Not a Valid User")
