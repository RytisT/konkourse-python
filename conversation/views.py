from django.http import HttpResponse
from django.utils import simplejson
from account.models import UserProfile
from conversation.models import ConversationPost, ConvoWall, ConversationComment
from notification.views import notifyComment, notifyPost


def post(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            wall = ConvoWall.objects.get(id=POST['id'])
            message = POST['message']
            if message == '':
                results = {'success': False}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            elif len(message) > 5000:
                results = {'success': False, 'error': 'invalid length'}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            post_type = POST['type']
            wallPost = ConversationPost(creator=request.user, wall=wall, message=message, post_type=post_type)
            wallPost.save()
            notifyPost(request=request, wall=wall, post=wallPost)
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def comment(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            convoPost = ConversationPost.objects.get(id=POST['id'])
            message = POST['message']
            if message == '':
                results = {'success': False}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            elif len(message) > 5000:
                results = {'success': False, 'error': 'invalid length'}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            comment = ConversationComment(creator=request.user, message=message, post=convoPost)
            comment.save()
            convoPost.comments.add(comment)
            convoPost.save()
            notifyComment(request=request, post=convoPost, comment=comment)
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def deletePost(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            convoPost = ConversationPost.objects.get(id=POST['id'])
            parent = convoPost.wall.getParent
            if convoPost.creator != request.user or (isinstance(parent, UserProfile) and parent.user != request.user):
                results = {'success': False}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            convoPost.deleted = True
            convoPost.save()
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


def deleteComment(request):
    results = {'success': False}
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            POST = request.POST
            comment = ConversationComment.objects.get(id=POST['id'])
            parent = comment.post.wall.getParent
            if comment.creator != request.user or comment.post != request.user or (isinstance(parent, UserProfile) and parent.user != request.user):
                results = {'success': False}
                json = simplejson.dumps(results)
                return HttpResponse(json, mimetype='application/json')
            comment.deleted = True
            comment.save()
            results = {'success': True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
