from datetime import timedelta
import urllib

from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.utils.http import urlquote
from django.core.signing import Signer
from django.core.signing import BadSignature

from konkourse import settings
from change_email.managers import ExpiredEmailChangeManager
from change_email.managers import PendingEmailChangeManager


class EmailChange(models.Model):

    """
A model to temporarily store an email adress change request.
"""
    new_email = models.EmailField(help_text=_('The new email address that'
                                              ' still needs to be confirmed.'),
                                  verbose_name=_('new email address'),)
    date = models.DateTimeField(auto_now_add=True,
                                help_text=_('The date and time the email '
                                            'address change was requested.'),
                                verbose_name=_('date'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                help_text=_('The user that has requested the'
                                            ' email address change.'),
                                verbose_name=_('user'),)
    site = models.ForeignKey(Site, blank=True, null=True)

    objects = models.Manager()
    expired_objects = ExpiredEmailChangeManager()
    pending_objects = PendingEmailChangeManager()

    class Meta:
        verbose_name = _('email address change request')
        verbose_name_plural = _('email address change requests')
        get_latest_by = "date"

    def __unicode__(self):
        return "%s" % self.user

    def get_absolute_url(self):
        return reverse('change_email_detail', kwargs={'pk': self.pk})

    def has_expired(self, seconds=None):
        """
Checks whether this request has already expired.

:kwarg int seconds: The number of seconds to calculate a
    :py:class:`datetime.timedelta` object.
    Defaults to :setting:`EMAIL_CHANGE_TIMEOUT`.
:returns: ``True`` if the request has already expired,
    ``False`` otherwise.
:rtype: bool
"""
        if not seconds:
            seconds = settings.EMAIL_CHANGE_TIMEOUT
        delta = timedelta(seconds=seconds)
        expiration_date = timezone.now() - delta
        return expiration_date >= self.date

    def check_signature(self, signature):
        """
Checks if

- the signature has not expired by calling :func:`has_expired`.
- the signature has not been tampered with by
  calling :func:`verify_signature`.

:arg str signature: The signature to check, as generated
    by :func:`make_signature`.
:returns: ``True`` if the check was successfully completed,
    ``False`` otherwise.
:rtype: bool
"""
        if not self.has_expired():
            return self.verify_signature(signature)
        return False

    def get_expiration_date(self, seconds=None):
        """
Returns the expiration date of an :model:`EmailChange` object by adding
a given amount of seconds to it.

:kwarg int seconds: The number of seconds to calculate a
    :py:class:`datetime.timedelta` object.
    Defaults to :setting:`EMAIL_CHANGE_TIMEOUT`.
:returns:  A :py:class:`datetime` object representing the expiration
    date.
:rtype: :py:obj:`.datetime`
"""
        if not seconds:
            seconds = settings.EMAIL_CHANGE_TIMEOUT
        delta = timedelta(seconds=seconds)
        return self.date + delta

    def make_signature(self):
        """
Generates a signature to use in one-time secret URL's
to confirm the email address change request.

:returns: A signature.
:rtype: str
"""
        signer = Signer()
        value = signer.sign(self.new_email)
        email, signature = value.split(':', 1)
        return signature

    def send_confirmation_mail(self):
        """
An instance method to send a confirmation mail to the new
email address.

The generation of a confirmation email will use three templates that
can be set in each project's settings:

* :setting:`EMAIL_CHANGE_HTML_EMAIL_TEMPLATE`
* :setting:`EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE`
* :setting:`EMAIL_CHANGE_TXT_EMAIL_TEMPLATE`

These templates will receive the following context variables:

``date``
    The date when the email address change was requested.

``timeout_days``
    The number of days remaining during which the request may
    be waiting for confirmation.

``current_site``
    An object representing the current site on which the user
    is logged in.  Depending on whether ``django.contrib.sites``
    is installed, this may be an instance of either
    ``django.contrib.sites.models.Site`` (if the sites
    application is installed) or
    ``django.contrib.sites.models.RequestSite`` (if
    not). Consult the documentation for the Django sites
    framework for details regarding these objects' interfaces.

``new_email``
    The new email address.

``signature``
    The confirmation signature for the new email address.

``user``
    The user that has requested the email address change.
"""
        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = RequestSite(request)
        subject = settings.EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE
        body_htm = settings.EMAIL_CHANGE_HTML_EMAIL_TEMPLATE
        body_txt = settings.EMAIL_CHANGE_TXT_EMAIL_TEMPLATE
        context = {'current_site': current_site,
                   'date': self.date,
                   'timeout_date': self.get_expiration_date(),
                   'new_email': self.new_email,
                   'protocol': settings.EMAIL_CHANGE_USE_HTTPS and 'https' or 'http',
                   'signature': self.make_signature(),
                   'user': self.user}
        subject = render_to_string(subject, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        text_message = render_to_string(body_txt, context)
        if settings.EMAIL_CHANGE_HTML_EMAIL:
            html_message = render_to_string(body_htm, context)
            msg = EmailMultiAlternatives(subject, text_message,
                                         settings.EMAIL_CHANGE_FROM_EMAIL,
                                         [self.new_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        else:
            send_mail(subject, text_message,
                      settings.EMAIL_CHANGE_FROM_EMAIL,
                      [self.new_email])

    def verify_signature(self, signature):
        """
Checks if the signature has been tampered with.

:arg str signature: The signature to check, as generated by
    :func:`make_signature`.
:returns: ``True`` if the signature has not been tampered with,
    ``False`` otherwise.
    :rtype: bool
    """
        signer = Signer()
        value = "%s:%s" % (self.new_email, signature)
        try:
            original = signer.unsign(value)
        except BadSignature:
            return False
        return True
