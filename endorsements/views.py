from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.context import Context
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render
from connections.models import Connection, ConnectionRequest
from django.utils import simplejson
from django.contrib.auth.models import User
from endorsements.models import Endorsement
from notification.views import notifyEndorsement

def endorse(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            owner = User.objects.get(id=POST['id'])
            if not Endorsement.objects.has_endorsed(owner=owner, endorser=request.user):
                e = Endorsement(owner=owner, endorser=request.user)
                e.save()
		notifyEndorsement(endorsee=owner, endorser=request.user, endorsement=e)
                results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
