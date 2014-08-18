"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""

from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from account.views import activate, register

urlpatterns = patterns('',
                       url(r'^post/$', 'conversation.views.post'),
                       url(r'^comment/$', 'conversation.views.comment'),
                       url(r'^deleteComment/$', 'conversation.views.deleteComment'),
                       url(r'^deletePost/$', 'conversation.views.deletePost'),
                       url(r'^endorse/$', 'endorsements.views.endorse'),
                       url(r'^account/login/$', 'account.views.login'),
                       url(r'^logout/$', 'account.views.logout'),
                       url(r'^(?P<username>[\w\.\-]+)$', 'account.views.profile'),
                       url(r'^(?P<username>[\w\.\-]+)/connect/$', 'connections.views.connect'),
                       url(r'^(?P<username>[\w\.\-]+)/info/$', 'account.views.profile_info'),
                       url(r'^(?P<username>[\w\.\-]+)/connections/$', 'account.views.profile_connections'),
                       url(r'^(?P<username>[\w\.\-]+)/courses/$', 'account.views.profile_courses'),
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='templates/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='templates/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='templates/registration_closed.html'),
                           name='registration_disallowed'),
                       (r'^activate/$', 'account.views.activate'),
                       )
