from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render
from documents.models import Document
import os
import mimetypes
from documents.forms import DocumentForm
from django.core.context_processors import csrf
from django.utils import simplejson
from django.conf import settings
from conversation.models import ConversationPost
from courses.models import Course


def download(request, file_id):
    doc = Document.objects.get(id=file_id)
    file = open(settings.MEDIA_ROOT + doc.file.name, "r")
    mimetype = mimetypes.guess_type(doc.file.name)[0]
    if not mimetype:
        mimetype = "application/octet-stream"

    response = HttpResponse(file.read(), mimetype=mimetype)
    response["Content-Disposition"]= "attachment; filename=%s" % doc.filename
    return response

def documents(request, course_id=-1):
    if (request.user.is_authenticated() and request.user.is_active):
        u = request.user
        courses = Course.objects.filter(course_users=u)
        if course_id < 0:
            documents = Document.objects.filter(course__in=courses)
        else:
            documents = Document.objects.filter(course__id=course_id)
        variables_for_template = {
            'name': u.first_name + ' ' + u.last_name,
            'username': request.user.username,
            'form': DocumentForm(),
            'documents': documents,
            'courses': courses,
            'course_id': course_id,
        }
        variables_for_template.update(csrf(request))
        return render(request, 'website/documents.html', variables_for_template,
            context_instance=RequestContext(request))
    else:
        return redirect("/")

def upload(request):
    if request.method == 'POST':
        doc = __upload_core(request)
    else:
        redirect("/")
    if isinstance(doc, Exception):
        return Exception()
        u = request.user
        name = u.first_name + ' ' + u.last_name
        username = request.user.username
        variables_for_template = {
            'name': name,
            'username': username,
        }
        return redirect('/documents/', variables_for_template)
    else:
        return Exception()


def __upload_core(request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            u = request.user
            doc = Document(owner=u)
            file = request.FILES['file']
            doc.filename = request.FILES['file'].name
            doc.save()
            doc.file.save('file_' + str(doc.id), file)
            return doc
        else:
            return Exception()


def _uploadDocument(doc, file):
    with open(settings.MEDIA_ROOT + '/' + doc.owner.username + '/file_' + str(doc.id) , 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    destination = File(destination)
    return destination



def delete_document(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            doc = Document.objects.get(id=POST['id'])
            if doc.owner != request.user:
                results = {'success': False}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            post = None
            # If a document was uploaded through a post, delete that post as well.
            try:
                post = ConversationPost.objects.get(document=doc)
            except:
                pass
            if post:
                post.deleted = True
                post.save()
            doc.deleted = True
            os.remove(settings.MEDIA_ROOT + doc.file.name)
            doc.save()
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def rename_document(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            doc = Document.objects.get(id=POST['id'])
            doc.filename = POST['newName']
            doc.save()
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
