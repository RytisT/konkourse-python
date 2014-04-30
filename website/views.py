from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.template.context import Context
from django.template import RequestContext
from django.shortcuts import render
from account.views import profile, _profile_context, index as account_index
from account.forms import AccountForm, AccountNameForm
from account.forms import EmailPreferencesForm
from change_email.forms import EmailChangeForm
from account.util import createImage
from courses.models import Course


def calendar(request):
    if request.user.is_authenticated() and request.user.is_active:
        first_name = request.user.first_name
        last_name = request.user.last_name
        username = request.user.username

        variables_for_template = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'courses': Course.objects.filter(course_users__username=username),

        }
    return render(request, 'website/calendar.html', variables_for_template,
        context_instance=RequestContext(request))


def wizard(request):
    if request.user.is_authenticated() and request.user.is_active:
        first_name = request.user.first_name
        last_name = request.user.last_name
        username = request.user.username
        _list = Course.objects.filter(course_users__username=username)
        from courses.views import chunks
        new_list = (chunks(_list, 2))

        variables_for_template = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'courses': new_list,
            'course_length': _list.count(),
        }

    return render(request, 'website/wizard.html', variables_for_template,
        context_instance=RequestContext(request))

def calendar_new_courseevent(request):
    t = loader.get_template('website/calendar_new_courseevent.html')
    return HttpResponse(t.render(Context()))

def calendar_new_event(request):
    t = loader.get_template('website/calendar_new_event.html')
    return HttpResponse(t.render(Context()))

def calendar_new_task(request):
    t = loader.get_template('website/calendar_new_task.html')
    return HttpResponse(t.render(Context()))

def calendar_new_event_invite(request):
    t = loader.get_template('website/calendar_new_event_invite.html')
    return HttpResponse(t.render(Context()))

def calendar_view_event(request):
    t = loader.get_template('website/calendar_view_event.html')
    return HttpResponse(t.render(Context()))

def calendar_view_task(request):
    t = loader.get_template('website/calendar_view_task.html')
    return HttpResponse(t.render(Context()))

def groups(request):
    t = loader.get_template('website/group.html')
    return HttpResponse(t.render(Context()))

def index(request):
    return account_index(request)

def main(request):
    t = loader.get_template('website/main.html')
    return HttpResponse(t.render(Context()))

def messages(request):
    t = loader.get_template('website/messages.html')
    return HttpResponse(t.render(Context()))

def learn(request):
    t = loader.get_template('website/learn.html')
    return HttpResponse(t.render(Context()))

def teach(request):
    t = loader.get_template('website/teach.html')
    return HttpResponse(t.render(Context()))

def privacy(request):
    t = loader.get_template('website/privacy.html')
    return HttpResponse(t.render(Context()))

def about(request):
    t = loader.get_template('website/about.html')
    return HttpResponse(t.render(Context()))

def accountsettings_courses(request):
    t = loader.get_template('website/accountsettings_courses.html')
    return HttpResponse(t.render(Context()))

def accountsettings_courses_specific(request):
    t = loader.get_template('website/accountsettings_courses_specific.html')
    return HttpResponse(t.render(Context()))

def accountsettings_groups(request):
    t = loader.get_template('website/accountsettings_groups.html')
    return HttpResponse(t.render(Context()))

def accountsettings_groups_specific(request):
    t = loader.get_template('website/accountsettings_groups_specific.html')
    return HttpResponse(t.render(Context()))

def accountsettings_privacy(request):
    t = loader.get_template('website/accountsettings_privacy.html')
    return HttpResponse(t.render(Context()))

def accountsettings_verify(request):
    t = loader.get_template('website/accountsettings_verify.html')
    return HttpResponse(t.render(Context()))

def accountsettings_profile(request):
    if request.user.is_authenticated():
        u = request.user
        p = request.user.get_profile()
        if request.method == 'POST':
            account_form = AccountForm(request.POST, request.FILES, instance=p)
            name_form = AccountNameForm(request.POST, instance=u)
            if account_form.is_valid() and name_form.is_valid():
                p = account_form.save()
                u = name_form.save()
                dimentions = (150, 150)
                if len(request.FILES) == 1:
                    image = request.FILES['image']
                    p.image.save(image.name, createImage(p.image, dimentions))
                return profile(request, u.username)
            else:
                variables = _profile_context(request, u.username)
                variables['account_form'] = account_form
                variables['name_form'] = name_form
                return render(request, 'website/accountsettings_profile.html', variables,
                    context_instance=RequestContext(request))
        else:
            variables = _profile_context(request, u.username)
            variables['account_form'] = AccountForm(instance=p)
            variables['name_form'] = AccountNameForm(instance=u)
            return render(request, 'website/accountsettings_profile.html', variables,
             context_instance=RequestContext(request))

def accountsettings_security(request):
    if request.user.is_authenticated():
        user_profile = request.user.get_profile() #returns the instance of the user profile model associated with that User and assigns it to object 'p'
        if request.method == 'POST': #if the form has been submitted
            form = EmailPreferencesForm(request.POST, instance=user_profile) #A form bound to post data
            if form.is_valid(): #if the form is valid
                user_profile = form #assign form to profile model associated with the user
                user_profile.save() #save profile model
                return render(request, 'website/accountsettings_security.html', {'form': form,}) #send user to settings page with updated info
            else:
                return render(request, 'website/accountsettings_security.html', {'form': form,}) #return user to settings page
        else: #if the form is not being submitted
            form = EmailPreferencesForm(instance=user_profile)
            return render(request, 'website/accountsettings_security.html', {'form': form,}) #show user settings with most recent info



