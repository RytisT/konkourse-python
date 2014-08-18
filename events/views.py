from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.template.context import Context, RequestContext
from django.core.context_processors import csrf
from django.utils import simplejson
from models import Event
from conversation.models import ConversationPost


def join_event(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            event = Event.objects.get(id=POST['id'])
            event.join_event(request.user.id)
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def leave_event(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            event = Event.objects.get(id=POST['id'])
            event.leave_event(request.user.id)
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def delete_event(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            event = Event.objects.get(id=POST['id'])
            post = None
            # Delete the post for the event as well.
            try:
                post = ConversationPost.objects.get(event=event)
            except:
                pass
            if post:
                post.deleted = True
                post.save()
            event.deleted = True
            event.save()
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
