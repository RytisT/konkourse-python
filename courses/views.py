from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from account.views import login
from models import Course
from website.views import index
from forms import CourseForm, CourseInitialForm
from account.util import createImage
from django.core.context_processors import csrf
from events.forms import EventForm
from events.models import Event
import datetime
from documents.forms import DocumentForm
from datetime import timedelta
from conversation.models import ConvoWall, ConversationPost
from documents.views import __upload_core
from documents.models import Document
from endless_pagination.decorators import page_template
from notification.views import notifyCreateEvent, notifyDocShareCourse
from page.models import Page


def _course_context(request, course_id):
    course = Course.objects.get(id=course_id)
    institution = Page.objects.get(title=course.institution)
    variables_for_template = {
        'name': request.user.first_name + ' ' + request.user.last_name,
        'image': course.image,
        'course_name': course.name,
        'course_number': course.number,
        'institution': institution,
        'description': course.about,
        'professor': course.professor,
        'course_id': course_id,
        'course_form': CourseInitialForm(),
        'courses': Course.objects.filter(course_users__username=request.user.username),
        'current_course': course,
        'section_number': course.course_id,
        'is_logged_in': True,
    }
    return variables_for_template


def _course_exists(request):
    form = CourseInitialForm(request.POST, request.FILES)
    if form.is_valid():
        section_number = ""
        if request.user.get_profile().school.title == "James Madison University":
            section_number = request.POST['course_id'].zfill(4)
        else:
            section_number = request.POST['course_id']
        try:
            course = Course.objects.get(
                number__iexact=request.POST['course_number'],
                course_id__iexact=section_number,
                institution__iexact=request.user.get_profile().school.title)
            return (True, course)
        except Course.DoesNotExist:
            wall = ConvoWall(wall_type=3)
            wall.save()
            course = Course(
                wall=wall,
                number=request.POST['course_number'],
                course_id=section_number,
                institution=request.user.get_profile().school.title)
            course.save()
        return (False, course)
    return (False, None)


@page_template('website/course/course_page.html')
def course(request, course_id,
           error_message='', template='website/course/course.html', extra_context=None):
    if not request.user.is_authenticated() or not request.user.is_active:
        return redirect(index)
    else:
        variables = _course_context(request, course_id)
        variables['event_form'] = EventForm()
        variables['doc_form'] = DocumentForm()
        c = Course.objects.get(id=course_id)
        posts = ConversationPost.objects.filter(wall=c.wall, deleted=False).order_by('created')
        variables['wall'] = c.wall
        variables['posts'] = posts.reverse()
        if error_message != '':
            variables['error_message'] = error_message
        variables.update(csrf(request))
        if extra_context is not None:
            variables.update(extra_context)
        return render_to_response(
            template, variables, context_instance=RequestContext(request))


def create(request):
    if not request.user.is_authenticated():
        return login(request)
    if request.method == 'POST':
        exists, c = get_or_add_course(request)
        if(c is None):
            return index(request)
        if(not exists):
            return course_info_edit(request, c.id)
        else:
            return course(request, c.id)
    return redirect(index)


def get_or_add_course(request):
    exists, c = _course_exists(request=request)
    if c is None:
        return (exists, c)
    c = Course.objects.get(id=c.id)
    c.add_student(request.user)
    return (exists, c)


def course_leave(request, course_id):
    c = Course.objects.get(id=course_id)
    if(c.in_course(request.user)):
        c.remove_student(request.user)
        return redirect(index)
    return redirect(404)


def course_info(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    course = Course.objects.get(id=course_id)
    variables = _course_context(request, course_id)
    variables['timeValue'] = course.time
    variables['semester'] = course.get_semester
    variables['credits'] = course.credits
    return render(request, 'website/course/course_info.html',
                  variables,
                  context_instance=RequestContext(request),
                  )


def course_info_edit(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    variables = _course_context(request, course_id)
    variables['form'] = CourseForm(instance=Course.objects.get(id=course_id))
    variables.update(csrf(request))
    return render(request, 'website/course/course_info_edit.html',
                  variables,
                  context_instance=RequestContext(request),
                  )


def course_update(request, course_id):
    if request.method == 'POST':
        c = Course.objects.get(id=course_id)
        form = CourseForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            u = request.user
            c = form.save()
            dimentions = (150, 150)
            if len(request.FILES) == 1:
                image = request.FILES['image']
                c.image.save(image.name, createImage(c.image, dimentions))
            name = u.first_name + ' ' + u.last_name
            username = request.user.username
            variables_for_template = {
                'name': name,
                'username': username,
            }
            return redirect('/course/' + str(course_id) + '/', variables_for_template)
        else:
            variables = _course_context(request, course_id)
            variables['form'] = form
            variables.update(csrf(request))
            return render(request, 'website/course/course_info_edit.html',
                          variables,
                          context_instance=RequestContext(request))


def create_event(request, course_id):
    if request.method == 'POST':
        variables = _course_context(request, course_id)
        c = Course.objects.get(id=course_id)
        e = Event()
        e.creator = request.user
        form = EventForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            e = form.save()
            c.add_event(e)
            e.join_event(request.user.id)
            c.save()
            wallPost = ConversationPost(creator=request.user, wall=c.wall, message="", post_type='E', event=e)
            wallPost.save()
            notifyCreateEvent(course=c, event=e)
            return redirect(course_events, course_id)
        else:
            variables['form'] = form
            variables.update(csrf(request))
            return course(request, course_id, "Invalid event creation fields!!")
    return redirect(index)


def course_documents(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    variables = _course_context(request, course_id)
    variables['documents'] = Document.objects.filter(course__id=course_id).order_by('modified')
    return render(request, 'website/course/course_documents.html',
                  variables,
                  context_instance=RequestContext(request),
                  )


def course_upload(request, course_id):
    doc = __upload_core(request)
    if isinstance(doc, Exception):
        return course(request, course_id, "Invalid document!")
    else:
        c = Course.objects.get(id=course_id)
        message = request.POST['message_post']
        wallPost = ConversationPost(creator=request.user, wall=c.wall, message=message, post_type='D', document=doc)
        wallPost.save()
        doc.course.add(c)
        doc.save()
        notifyDocShareCourse(document=doc, course=c)
    return redirect(course_documents, course_id)


def course_events(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    variables = _course_context(request, course_id)
    today = datetime.date.today()
    week1_end = today + timedelta(days=6 - today.weekday())
    week2_end = week1_end + timedelta(days=7)
    c = Course.objects.get(id=course_id)
    variables['thisWeek'] = c.events.filter(start_date__range=[today, week1_end], deleted=False)
    variables['nextWeek'] = c.events.filter(start_date__gt=week1_end, start_date__lte=week2_end, deleted=False)
    variables['future'] = c.events.filter(start_date__gt=week2_end, deleted=False)
    return render(request, 'website/course/course_events.html',
                  variables,
                  context_instance=RequestContext(request),
                  )


def course_members(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    template_variables = _course_context(request, course_id)
    c = Course.objects.get(id=course_id)
    _list = c.course_users.filter(courseuser__role='S')
    new_list = (chunks(_list, 3))
    template_variables['course_members'] = new_list
    template_variables['user'] = request.user
    return render(request, 'website/course/course_members.html',
                  template_variables,
                  context_instance=RequestContext(request),
                  )


def course_gradebook(request, course_id):
    if not request.user.is_authenticated():
        return login(request)
    return render(request, 'website/course/course_gradebook.html',
                  _course_context(request, course_id),
                  context_instance=RequestContext(request),
                  )


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

from django.http import HttpResponse
from django.utils import simplejson


def add_course(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            courses = Course.objects.filter(course_users__username=request.user.username)
            if courses.count() >= 10:
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            exists, c = get_or_add_course(request)
            if c is not None:
                results = {'success': True}
            else:
                results = {'success': False}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
