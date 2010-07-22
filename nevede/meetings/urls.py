# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Fondazione Bruno Kessler (www.fbk.eu), 2008-2010

from django.conf.urls.defaults import *
from nevede.meetings.forms import CreateMeetingWizard, CreateMeetingForm_1, \
     CreateMeetingForm_2

urlpatterns = patterns('nevede.meetings.views',
    (r'^$', 'index'),
    (r'^create/$', CreateMeetingWizard(
        [CreateMeetingForm_1, CreateMeetingForm_2])),
    (r'^list/$', 'list'),
    (r'^view/(?P<m_id>\d+)/$', 'detail'),
)
