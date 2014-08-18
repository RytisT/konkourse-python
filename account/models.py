from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from page.models import Page
from conversation.models import ConvoWall
from messages.models import Inbox


def getPath(instance, filename):
    path = 'user_' + str(instance.id) + '/' + filename
    return path


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
        ('E', 'Extraterrestrial'),
        ('O', 'Other'),
    )
    user = models.ForeignKey(User, unique=True)
    wall = models.ForeignKey(ConvoWall, unique=True, related_name='Wall')
    messages = models.ForeignKey(Inbox, unique=True, related_name='Messages')
    image = models.ImageField(upload_to=getPath)
    birthday = models.DateField(blank=True, null=True, name="birthday")
    education = models.CharField(max_length=100)
    major = models.CharField(max_length=50, default="Undeclared")
    tagline = models.CharField(blank=True, max_length=200)
    phone_number = models.CharField(blank=True, max_length=12)
    about = models.CharField(max_length=1000, blank=True)
    interests = models.CharField(max_length=1000, blank=True)
    school = models.ForeignKey(Page, related_name='School')
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, default='E')
    modified = models.DateTimeField(auto_now=True)
    first_time = models.BooleanField(default=True)
    connection_request_email = models.BooleanField(default=True)
    endorsement_email = models.BooleanField(default=True)
    profile_post_email = models.BooleanField(default=True)
    course_post_email = models.BooleanField(default=True)
    new_course_member_email = models.BooleanField(default=True)

    def getImage(self):
        if self.image:
            return self.image.url
        else:
            char = self.user.last_name[-1]
            num = str((ord(char) % 26) + 1)
            if len(num) == 1:
                num = '0' + num
            return '%simg/cats/00' % settings.STATIC_URL + num + '.jpg'


def getSchool(self):
    virginia_tech = Page.objects.get(title='Virginia Tech')
    jmu = Page.objects.get(title='James Madison University')
    uva = Page.objects.get(title='University of Virginia')
    konkourse = Page.objects.get(title='Konkourse')
    emailLookup = {
        'vt.edu': virginia_tech,
        'jmu.edu': jmu,
        'dukes.jmu.edu': jmu,
        'virginia.edu': uva,
        'konkourse.com': konkourse,
    }
    parts = self.split('@')
    school = emailLookup[parts[1]]
    return school


def send_endorsement_email(endorser_name, endorsee_name, endorsee_email):
    from templated_email import send_templated_mail
    send_templated_mail(
        template_name='new_endorsement',
        from_email='admin@konkourse.com',
        recipient_list=[endorsee_email],
        context={
            'endorser_name': endorser_name,
            'endorsee_name': endorsee_name,
        },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )
