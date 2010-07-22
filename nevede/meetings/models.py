# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Davide Setti, 2008

import datetime
from django.db.models import *
from django_extensions.db.models import TimeStampedModel

class Meeting(TimeStampedModel):
    title = CharField(max_length=200)
    description = CharField(max_length=2000, blank = True)
    author_email = EmailField(max_length=100, blank = True)
    private = BooleanField(default=False)
    hidden_id = CharField(max_length=45, blank = True)
    
    class Meta():
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    def save(self):
        from random import randint

        if not self.pk:
            hid = randint(0,10**30)
            while Meeting.objects.filter(hidden_id__exact=str(hid)).exists():
                hid = randint(0,10**30)
            self.hidden_id = str(hid)

        super(Meeting, self).save()

    @permalink
    def get_absolute_url(self):
        return ('nevede.meetings.views.detail', (), {
            'm_id': self.hidden_id
        })

class Choice(TimeStampedModel):
    meeting = ForeignKey(Meeting)
    text = CharField(max_length=200) 
    date = DateField(null = True)
    hour_start = DateTimeField(null = True)
    hour_end = DateTimeField(null = True)
    location = CharField(max_length=2000, null = True)

    def __unicode__(self):
        return "%s: %s" % (self.meeting.title, self.text)


class Participation(TimeStampedModel):
    user = CharField(max_length=30)
    choice = ForeignKey(Choice)
    present = BooleanField(default=False)

    def __unicode__(self):
        return u"%s chose %s in meeting %s" %(self.user, self.choice.text,
                                               self.choice.meeting.title)
