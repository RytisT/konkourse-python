from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.models import User
from account.models import UserProfile
from courses.models import Course
from notifications import notify
from django.core.mail import send_mail
from account.models import send_endorsement_email


def updates(request):
    if (request.user.is_authenticated() and request.user.is_active):
        u = request.user
        name = u.first_name + ' ' + u.last_name
        username = request.user.username
        request.user.notifications.mark_all_as_read()
        notifications = request.user.notifications.all()

        variables_for_template = {
            'name': name,
            'user': u,
            'username': username,
            'notifications': notifications,
        }
        return render(request, 'website/updates.html', variables_for_template,
                      context_instance=RequestContext(request))
    else:
        return Exception()


def notifyCourseJoin(course, newMember):
    course_users = course.course_users.all()
    for user in course_users:
        notify.send(newMember, recipient=user, action_object=course, verb='joined')


def notifyEndorsement(endorsee, endorser, endorsement):
    notify.send(endorser, recipient=endorsee, action_object=endorsement, verb='endorsed')
    if UserProfile.endorsement_email is True:
        endorser_name = endorser.first_name + ' ' + endorser.last_name
        endorsee_name = endorsee.first_name
        endorsee_email = endorsee.email
        send_endorsement_email(endorser_name, endorsee_name, endorsee_email)


def notifyCreateEvent(event, course):
    course_users = course.course_users.all()
    for user in course_users:
        if user != event.creator:
            notify.send(event.creator, recipient=user, action_object=event, verb='created an event', target=course)


def notifyDocShareCourse(document, course):
    course_users = course.course_users.all()
    for user in course_users:
        if user != document.owner:
            notify.send(document.owner, recipient=user, action_object=document, verb='shared a doc', target=course)


from conversation.models import ConversationPost, ConvoWall, ConversationComment


def notifyComment(request, post, comment):
    # Send notifications to involved parties.
    recipient = post.creator
    if recipient != request.user:
        # sends a notification to the owner of the post.
        notify.send(request.user, recipient=recipient, action_object=comment, verb='commented on', target=post,
                    description=comment.message)
    # Send notifications to every unique user who commented on the post.
    values = ConversationComment.objects.filter(post=post).values("creator").distinct()
    for value in values:
        user = User.objects.get(id=value["creator"])
        if user != post.creator and user != comment.creator:
            notify.send(request.user, recipient=user, action_object=comment, verb='commented on', target=post,
                        description=comment.message)
    # Send notification to wall owner.
   # wallOwner = post.wall.getParent.user
    # if recipient != wallOwner:
    #    print


def notifyPost(request, post, wall):
    if wall.wall_type == 0:
        user = UserProfile.objects.get(wall=wall).user
        if user != request.user:
            notify.send(request.user, recipient=user, action_object=post, verb='posted on', target=user.get_profile(),
                        description=post.message)
    elif wall.wall_type == 3:
        course = Course.objects.get(wall=wall)
        course_users = course.course_users.all()
        for user in course_users:
            if user != request.user:
                notify.send(
                    request.user,
                    recipient=user,
                    action_object=post,
                    verb='posted on course',
                    target=course,
                    description=post.message)
