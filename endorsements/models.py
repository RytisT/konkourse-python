from django.db import models
from django.contrib.auth.models import User


class EndorsementManager(models.Manager):
    def get_endorsements(self, user):
        endorsements = self.filter(owner=user).select_related(depth=1)
        return endorsements
    def has_endorsed(self, owner, endorser):
        try:
            endorsement = Endorsement.objects.get(owner=owner, endorser=endorser)
            return True
        except:
            return False

class Endorsement(models.Model):
    owner = models.ForeignKey(User, related_name="owner_endorsement")
    created = models.DateTimeField('created', auto_now_add=True)
    objects = EndorsementManager()
    endorser = models.ForeignKey(User, related_name="endorser_endorsement")
    comment = models.TextField(default="")
    
    def getObjectType(self):
        return "Endorsement"


