from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from change_email.models import EmailChange
from change_email.validators import validate_email_not_used


class EmailChangeForm(forms.ModelForm):
    """
A form to allow users to change the email address they have
registered with.

Just consists of an ``forms.EmailField`` with a
:validator:`validate_email_not_used` validator to check if a
given email address is not already used.
"""
    new_email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':""}),
                                 validators=[validate_email_not_used])

    class Meta:
        model = EmailChange
        exclude = ('user', 'site')
