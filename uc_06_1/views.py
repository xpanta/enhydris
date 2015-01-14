from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page
import requests
from json import loads


@login_required
def get_plegma_devices(request, username):
    user = request.user
    sock_url = ""
    sockets = []
    if username == user.username and user.username == 'GR006047':
        _type = request.GET.get("t", "")
        res = requests.get('http://iwidget.plegmalabs.com/'
                           'rest/sitemaps/demo/demo/?type=json',
                           auth=('demo', 'demo'))
        _json = loads(res.text)
        _arr = _json.get("widget")
        dev_label = request.GET.get("d", "")
        _next = request.GET.get("n", "")
        if dev_label and _next:  # toggle device
            headers = {"Content-Type": "text/plain"}
            url = 'http://iwidget.plegmalabs.com/rest/items/%s' % dev_label
            res = requests.post(url, auth=('demo', 'demo'),
                                data=_next, headers=headers)
        for item in _arr:
            if item.get("label").upper() == _type.upper():
                page = item.get("linkedPage")
                sock_url = page.get("link")
                break
        if sock_url:
            res = requests.get('%s?type=json' % sock_url, auth=('demo', 'demo'))
            _json = loads(res.text)
            widgets = _json.get("widget")
            try:
                # Create the sockets.
                for widget in widgets:
                    try:
                        item = widget.get("item", "")
                        _type = item.get("type")
                    except (AttributeError, ValueError, KeyError):
                        continue
                    if _type == "SwitchItem":
                        label = widget.get("label")
                        label = label[0:label.find("status")-1]
                        state = item.get("state")
                        name = item.get("name")
                        if state == "ON":
                            _next = "OFF"
                        elif state == 'OFF':
                            _next = "ON"
                        socket = {
                            "label": label,
                            "state": state,
                            "next": _next,
                            "name": name,
                        }
                        sockets.append(socket)
                # add consumptions
                for widget in widgets:
                    try:
                        item = widget.get("item", "")
                        _type = item.get("type")
                    except (AttributeError, ValueError, KeyError):
                        continue
                    label = widget.get("label")
                    if "Total Energy" in label and _type == "NumberItem":
                        consumption = item.get("state")
                        label = label[0:label.find("Total Energy")-1]
                        for socket in sockets:
                            if socket.get("label") == label:
                                socket["consumption"] = consumption
            except Exception as e:
                import logging
                log = logging.getLogger(__name__)
                log.debug("Error in getting Plegma Devices %s" % repr(e))
        data = {
            "sockets": sockets,
            "username": username,
        }
        variables = RequestContext(request, data)
        return render_to_response("_devices_.html", variables)
