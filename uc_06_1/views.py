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
            _arr = _json.get("widget")
            socket1 = {"text": "Plug1"}
            socket2 = {"text": "Plug2"}
            for a in _arr:
                item = a.get("item", "")
                try:
                    s_type = item.get("type")
                    if item:
                        name = item.get("name")
                        if name == "Zwave2" and s_type == "SwitchItem":
                            state = item.get("state")
                            socket1["label"] = "Zwave2"
                            if state == "ON":
                                # Warning this is opposite for UI reasons
                                socket1["state"] = "OFF"
                            else:
                                socket1["state"] = "ON"
                        if name == "Zwave3" and s_type == "SwitchItem":
                            state = item.get("state")
                            socket2["label"] = "Zwave3"
                            if state == "ON":
                                socket2["state"] = "OFF"
                            else:
                                socket2["state"] = "ON"
                        if name == "Zwave2b" and s_type == "NumberItem":
                            state = item.get("state")
                            socket1["consumption"] = state
                        if name == "Zwave3b" and s_type == "NumberItem":
                            state = item.get("state")
                            socket2["consumption"] = state
                except Exception as e:
                    import logging
                    log = logging.getLogger(__name__)
                    log.debug("Error in getting Plegma Devices %s" % repr(e))
            sockets.append(socket1)
            sockets.append(socket2)
        data = {
            "sockets": sockets,
            "username": username,
        }
        variables = RequestContext(request, data)
        return render_to_response("_devices_.html", variables)
