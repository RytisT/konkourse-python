# TODO: Remove connection

from django.http import HttpResponse
from django.template.context import Context
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render
from connections.models import Connection, ConnectionRequest
from django.utils import simplejson
from django.contrib.auth.models import User
from account import views


def accept(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            if u'id' in POST:
                id = int(POST[u'id'])
                conReq = ConnectionRequest.objects.get(id=id)
                conReq.accept()
                results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def hide(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            if u'id' in POST:
                id = int(POST[u'id'])
                conReq = ConnectionRequest.objects.get(id=id)
                conReq.hidden = True
                conReq.save()
                results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def connect(request, username):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            u = User.objects.get(username=username)
            if Connection.objects.connected(request.user, u) or ConnectionRequest.objects.requestSent(request.user, u) or ConnectionRequest.objects.requestReceived(request.user, u):
                return views.profile(request, username)
            connectReq = ConnectionRequest(creator=request.user, reciever=u)
            connectReq.save()
        return views.profile(request, username)
    else:
        return views.index(request)
