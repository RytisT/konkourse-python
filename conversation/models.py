from django.db import models
from django.contrib.auth.models import User


class ConversationManager(models.Manager):
    def getWallPosts(self, user):
        posts= []
        relations = self.filter(reciever=user).select_related(depth=1)
        for post in relations:
            posts.append({"creator": post.creator, "post": post })

        return posts

class ConvoWall(models.Model):
    TYPE = (
        (0, 'User'),
        (1, 'Group'),
        (2, 'Event'),
        (3, 'Course'),
        (4, 'Message'),
    )
    wall_type = models.SmallIntegerField(choices=TYPE)

    def getObjectType(self):
        return "ConvoWall"

    def getParent(self):
        from account.models import UserProfile
        from courses.models import Course
        if self.wall_type == 0:
            return UserProfile.objects.get(wall=self)
        elif self.wall_type == 3:
            return Course.objects.get(wall=self)



class ConversationComment(models.Model):
    CONVERSATION_TYPES=(
    ('P', 'Post'),
    ('I', 'Image'),
    ('L', 'Link'),
    ('O', 'Other'),
    ('E', 'Event'),
    ('D', 'Document'),
    )
    type = models.CharField(max_length=1, choices=CONVERSATION_TYPES)
    created = models.DateTimeField('created', auto_now_add=True)
    creator = models.ForeignKey(User, related_name='comment_creator')
    message = models.TextField(default="")
    deleted = models.BooleanField(default=False)
    post = models.ForeignKey('ConversationPost', related_name="comment_post")

    def getObjectType(self):
        return "ConversationComment"

from documents.models import Document
from events.models import Event

class ConversationPost(models.Model):
    CONVERSATION_TYPES=(
    ('P', 'Post'),
    ('I', 'Image'),
    ('L', 'Link'),
    ('O', 'Other'),
    ('E', 'Event'),
    ('D', 'Document'),
    )
    post_type = models.CharField(max_length=1, choices=CONVERSATION_TYPES)
    document = models.ForeignKey(Document, null=True, related_name='posted_document')
    event = models.ForeignKey(Event, null=True, related_name='posted_event')
    created = models.DateTimeField('created', auto_now_add=True)
    creator = models.ForeignKey(User, related_name='post_creator')
    wall = models.ForeignKey(ConvoWall, related_name='wall')
    message = models.TextField(default="")
    objects = ConversationManager()
    comments = models.ManyToManyField(ConversationComment)
    deleted = models.BooleanField(default=False)

    def getObjectType(self):
        return "ConversationPost"

    def isOnOwnWall(self):
        from account.models import UserProfile
        wallOwner = UserProfile.objects.get(wall=self.wall).user
        return self.creator == wallOwner


