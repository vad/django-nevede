# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Fondazione Bruno Kessler (www.fbk.eu), 2008-2010

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/meetings/'}),
    (r'^meetings/', include('nevede.meetings.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^meetings/media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    
