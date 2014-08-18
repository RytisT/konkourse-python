from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from conversation.models import ConvoWall


def getPath(instance, filename):
    path = 'course_' + str(instance.id) + '/' + filename
    return path


class Course(models.Model):
    course_users = models.ManyToManyField(User, through='CourseUser')
    image = models.ImageField(upload_to=getPath)
    name = models.CharField(default="Name me!", max_length=200)
    number = models.CharField(max_length=10)
    professor = models.CharField(max_length=100, default="Who Knows!")
    about = models.TextField(default="A course about something.")
    institution = models.CharField(max_length=200)
    time = models.TimeField(blank=True, null=True)
    course_id = models.CharField(max_length='10')
    semester = models.CharField(max_length="4", default="None")
    credits = models.CharField(max_length="1", default="3")
    tag = models.CharField(max_length="100", default="I love konkourse!")
    events = models.ManyToManyField(Event)
    wall = models.ForeignKey(ConvoWall, unique=True, related_name='Conversation_Wall')

    def __unicode__(self):
        return self.name

    def in_course(self, user):
        if user not in self.course_users.filter(courseuser__user=user):
            return False
        else:
            return True

    def get_semester(self):
        SEMESTER_OPTIONS = (
            ('S013', 'Spring 2013'),
            ('M113', 'Summer I 2013'),
            ('M213', 'Summer II 2013'),
            ('F013', 'Fall 2013'),
            ('S014', 'Spring 2014'),
        )
        for sem in SEMESTER_OPTIONS:
            if sem[0] == self.semester:
                return sem[1]
        return "None"

    def add_student(self, user):
        if(user not in self.course_users.filter(courseuser__user=user)):
            from notification.views import notifyCourseJoin
            notifyCourseJoin(course=self, newMember=user)
            s = CourseUser(user=user, course=self, role='S')
            s.save()

    def remove_student(self, user):
        s = self.courseuser_set.get(user=user)
        s.delete()

    def add_event(self, event):
        self.events.add(event)

    def remove_event(self, event):
        self.events.delete(event)

    def getObjectType(self):
        return "Course"


class CourseUser(models.Model):
    COURSE_ROLE = (
        ('I', 'instructor'),
        ('A', 'assistant'),
        ('S', 'student'),
    )

    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    role = models.CharField(max_length=1, choices=COURSE_ROLE)

    def __unicode__(self):
        return unicode(self.course) + ':' + unicode(self.user)


def course_users(course_id):
    course_users = CourseUser.objects.filter(role='S', course__id=course_id)
    return course_users
