# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from django.template import RequestContext
from django.shortcuts import redirect
from django.shortcuts import render
from conversation.models import ConvoWall, ConversationPost

def messages(request):
	if request.user.is_authenticated():
		first_name = request.user.first_name 
		last_name = request.user.last_name
		username = request.user.username
		messageWall = request.user.get_profile().messages
		messages = ConversationPost.objects.filter(wall=request.user.get_profile().messages)

		variables_for_template = {
			'first_name': first_name,
			'last_name': last_name,
			'username': username,
			'messages': messages,
			'messageWall': messageWall,
		}
		return render(request, 'website/messages.html', variables_for_template, 
			context_instance=RequestContext(request))

def messages_compose(request):
	if request.user.is_authenticated():
		first_name = request.user.first_name 
		last_name = request.user.last_name
		username = request.user.username
		messageWall = request.user.get_profile().messages
		messages = ConversationPost.objects.filter(wall=request.user.get_profile().messages)

		variables_for_template = {
			'first_name': first_name,
			'last_name': last_name,
			'username': username,
			'messages': messages,
			'messageWall': messageWall,
		}
		return render(request, 'website/messages_compose.html', variables_for_template, 
			context_instance=RequestContext(request))

def messages_view(request):
	if request.user.is_authenticated():
		first_name = request.user.first_name 
		last_name = request.user.last_name
		username = request.user.username
		messageWall = request.user.get_profile().messages
		messages = ConversationPost.objects.filter(wall=request.user.get_profile().messages)

		variables_for_template = {
			'first_name': first_name,
			'last_name': last_name,
			'username': username,
			'messages': messages,
			'messageWall': messageWall,
		}
		return render(request, 'website/messages_view.html', variables_for_template, 
			context_instance=RequestContext(request))
