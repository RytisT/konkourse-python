from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^account/', include('change_email.urls')),
                       )
