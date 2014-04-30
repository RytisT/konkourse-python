from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length='55')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length='60')
    description = models.TextField(max_length='500')
    members = models.ManyToManyField(User)
    created = models.DateTimeField('created', auto_now_add=True)
    creator = models.ForeignKey(User, related_name='event_creator')
    deleted = models.BooleanField(default=False)

    def join_event(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            raise Exception("Non existing user tried to join event.")
        if user not in self.members.all():
            self.members.add(user)
            return True
        return False

    def leave_event(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            raise Exception("Non existing user tried to leave event.")
        if user in self.members.all():
            self.members.remove(user)
            return True
        return False

    def getObjectType(self):
        return "Event"

    def __unicode__(self):
        return str(self.start_date) + "_" + str(self.id)

    def getParent(self):
        return self.course_set.all()[0]

