from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from account.models import UserProfile, getSchool
from django.shortcuts import redirect
from django.template import RequestContext
from connections.models import Connection, ConnectionRequest
from conversation.models import ConvoWall, ConversationPost
from courses.models import Course
from courses.forms import CourseInitialForm
from django.core.context_processors import csrf
from endorsements.models import Endorsement
from messages.models import Inbox
from endless_pagination.decorators import page_template
from activation.models import RegistrationProfile
from forms import AccountInitialForm
import datetime
from datetime import timedelta
from events.models import Event
from django.db.models import Q
from itertools import chain


@page_template('website/main_page.html')
def index(request,
          template='website/main.html', extra_context=None):
    if not (request.user.is_authenticated() and request.user.is_active):
        return redirect(login)
    today = datetime.date.today()
    one_week = today + timedelta(days=today.weekday() + 7)
    events = Event.objects.filter(
        start_date__range=[
            today,
            one_week],
        members__id__exact=request.user.id,
        deleted=False).order_by('start_date')
    walls = []
    walls.append(request.user.get_profile().wall)
    connections = Connection.objects.getConnections(request.user)
    for con in connections:
        walls.append(con.get_profile().wall)
    courses = Course.objects.filter(course_users__username=request.user.username)
    for course in courses:
        walls.append(course.wall)
    posts = ConversationPost.objects.filter(Q(~Q(creator=request.user),
                                              wall__in=walls,
                                              deleted=False) | Q(creator__is_staff=True,
                                                                 deleted=False)).distinct().order_by('created')
    variables_for_template = {
        'name': request.user.first_name + ' ' + request.user.last_name,
        'username': request.user.username,
        'conReqs': [x['request'] for x in ConnectionRequest.objects.getRequests(request.user)],
        'courses': courses,
        'form': CourseInitialForm(),
        'events': events,
        'posts': posts.reverse(),
    }
    if extra_context is not None:
        variables_for_template.update(extra_context)
    return render_to_response(template, variables_for_template, context_instance=RequestContext(request))


def login(request):
    variables_for_template = {
        'form': AccountInitialForm(),
    }
    variables_for_template.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            variables_for_template["error_message"] = "Inavlid username or password."
            return render(
                request,
                'website/login.html',
                variables_for_template,
                context_instance=RequestContext(request))
        if user.is_active == False:
            variables_for_template["error_message"] = "Account hasn't been activated. Check your email!"
            return render(
                request,
                'website/login.html',
                variables_for_template,
                context_instance=RequestContext(request))
        auth_login(request, user)
    if request.user.is_authenticated() and request.user.is_active:
        if request.user.get_profile().first_time:
            from website.views import wizard
            return wizard(request)
        return redirect('/')
    return render(request, 'website/login.html', variables_for_template, context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)
    variables_for_template = {
        'form': AccountInitialForm()
    }
    variables_for_template.update(csrf(request))
    return render(request, 'website/login.html', variables_for_template)


def register(request, template_name='templates/website/register.html'):
    if request.user.is_authenticated() and request.user.is_active:
        return redirect('/')
    variables_for_template = {}
    form = AccountInitialForm(request.POST, request.FILES)
    if request.method == 'POST':
        variables_for_template = {
            'form': form,
        }
        variables_for_template.update(csrf(request))
        if form.is_valid():
            user = form.save()
            user = RegistrationProfile.objects.create_inactive_user(new_user=user,
                                                                    site=Site.objects.get_current())
            return render(request, 'website/activate_email_sent.html', variables_for_template)
    return render(request, 'website/login.html', variables_for_template)


def activate(request, activation_key, template_name='activate.html'):
    account = RegistrationProfile.objects.activate_user(activation_key)
    if account:
        wall = ConvoWall(wall_type=0)
        wall.save()
        inbox = Inbox(owner=account)
        inbox.save()
        profile, created = UserProfile.objects.get_or_create(user=account,
                                                             wall=wall, messages=inbox, school=getSchool(account.email))
        profile.save()
        return render(request, 'website/activate.html')
    # TODO: Handle invalid activations i.e. clicking on the link more then once or expired links
    else:
        return render(request, 'website/activate.html')


# TODO: Implement reset
def reset(request):
    return render(request, 'website/reset.html')


def _profile_context(request, username):
    u = User.objects.get(username=username)
    profile = u.get_profile()
    if profile.first_time and request.user == u:
        first_time = True
        profile.first_time = False
        profile.save()
    else:
        first_time = False
    variables_for_template = {
        'name': u.first_name + ' ' + u.last_name,
        'username': u.username,
        'education': u.get_profile().school.title,
        'major': u.get_profile().major,
        'tagline': u.get_profile().tagline,
        'image': u.get_profile().getImage(),
        'requestS': ConnectionRequest.objects.requestSent(request.user, u),
        'requestR': ConnectionRequest.objects.requestReceived(request.user, u),
        'wall': u.get_profile().wall,
        'connections': Connection.objects.getConnections(u),
        'courses': Course.objects.filter(course_users__username=username),
        'endorsements': Endorsement.objects.get_endorsements(u),
        'id': u.id,
        'first_time': first_time,
        'has_endorsed': Endorsement.objects.has_endorsed(owner=u, endorser=request.user),
    }
    return variables_for_template


@page_template('website/profile/base_profile_page.html')
def profile(request, username,
            template='website/base_profile.html', extra_context=None):
    if request.user.is_authenticated() and request.user.is_active:
        u = get_object_or_404(User, username=username)
        connected = Connection.objects.connected(u, request.user)
        context = _profile_context(request, username)
        if not connected and not (u.username == request.user.username):
            template = 'website/profile/profile_restricted.html'
        else:
            posts = ConversationPost.objects.filter(wall=u.get_profile().wall, deleted=False).order_by('created')
            context['posts'] = posts.reverse()
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))
    else:
        return redirect('/')


def profile_info(request, username):
    if request.user.is_authenticated() and request.user.is_active:
        u = get_object_or_404(User, username=username)
        connected = Connection.objects.connected(u, request.user)
        if not connected and not (u.username == request.user.username):
            return redirect(profile, username)
        variables = {
            'email': u.email,
            'interests': u.get_profile().interests,
            'about': u.get_profile().about,
            'number': u.get_profile().phone_number,
            'sex': u.get_profile().sex,
            'birthday': u.get_profile().birthday,
        }
        variables = dict(_profile_context(request, username).items() + variables.items())
        return render(request, 'website/profile/profile_info.html', variables,
                      context_instance=RequestContext(request))
    else:
        return redirect('/')


def profile_courses(request, username):
    if request.user.is_authenticated() and request.user.is_active:
        u = get_object_or_404(User, username=username)
        connected = Connection.objects.connected(u, request.user)
        if not connected and not (u.username == request.user.username):
            return redirect(profile, username)
        return render(request, 'website/profile/profile_currentcourse.html', _profile_context(request, username),
                      context_instance=RequestContext(request))
    else:
        return redirect('/')


def profile_connections(request, username):
    if request.user.is_authenticated() and request.user.is_active:
        u = get_object_or_404(User, username=username)
        connected = Connection.objects.connected(u, request.user)
        if not connected and not (u.username == request.user.username):
            return redirect(profile, username)
        variables = _profile_context(request, username)
        return render(request, 'website/profile/profile_connections.html', variables,
                      context_instance=RequestContext(request))
    else:
        return redirect('/')
