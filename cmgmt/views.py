from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render


def coursemgmt(request):
    if request.user.is_authenticated() and request.user.is_active:
        first_name = request.user.first_name 
        last_name = request.user.last_name
        username = request.user.username
   
        variables_for_template = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
        }
    return render(request, 'website/coursemgmt.html', variables_for_template, 
        context_instance=RequestContext(request))
