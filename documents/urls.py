from django.conf.urls import patterns, url

# All urls are subject to change once the course identification system is up.
urlpatterns = patterns('',
                       url(r'^documents/$', 'documents.views.documents'),
                       url(r'^documents/filter/(?P<course_id>\w+)/$', 'documents.views.documents'),
                       url(r'^upload/$', 'documents.views.upload'),
                       url(r'^renameDocument/$', 'documents.views.rename_document'),
                       url(r'^deleteDocument/$', 'documents.views.delete_document'),
                       url(r'^documents/(?P<file_id>\w+)/$', 'documents.views.download'),
                       )
