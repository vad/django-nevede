# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Davide Setti, 2008-2010

import sys
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.paginator import Paginator
from django.template import RequestContext
from nevede.meetings.models import Meeting, Choice, Participation
from nevede.meetings.email import *


def index(request):
    latest_m = Meeting.objects.filter(private=False).order_by('-created')[:5]

    return render_to_response('index.html', {
            'meetings': latest_m,
        },
        context_instance=RequestContext(request)
    )


def list(request):
    latest_m = Meeting.objects.filter(private=False).order_by('-created')

    format = request.GET.get('format', '')
    callback = request.GET.get('callback', '')
    nPage = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    
    ##pagination
    p = Paginator(latest_m, int(limit))
    page = p.page(nPage)
    latest_m = page.object_list

    if format == "json" or format == "xml":
        serializer = serializers.get_serializer(format)()
        serializer.serialize(latest_m, ensure_ascii=False,
            fields=('pk','title', 'hidden_id', 'created', 'modified'))
        data = serializer.getvalue()
        if format == 'json':
            data = "{totalProperty: %d, meetings: %s}" % (p.count, data)
            if callback and format == 'json':
                data = "%s(%s)" % (callback, data)
        return HttpResponse(data)
    
    return render_to_response('meetings/list.html', {
            'meetings': latest_m,
            'path': '../',
        },
        context_instance=RequestContext(request)
    )


def detail(request, m_id):
    from datetime import datetime

    def unique(seq): # Dave Kirby, Order preserving
        ##TODO: use python 2.7 order preserving set if available
        seen = set()
        return [x for x in seq if x not in seen and not seen.add(x)]


    m = get_object_or_404(Meeting, hidden_id=m_id)
    choices = Choice.objects.filter(meeting__hidden_id=m_id).order_by('date', 'pk')
    
    if request.session.get('meeting_created'):
        created_now = True
        del request.session['meeting_created']
    else:
        created_now = False

    if request.method == 'POST': # If the form has been submitted...
        created_now = True
        username = 'Unknown'
        if request.POST['username']:
            username = request.POST['username']

        for c in choices:
            present = '%d'%c.pk in request.POST.getlist('choices')

            p = Participation(choice=c, user=username,
                    present=present)
            p.save()
    
        if m.author_email:
            send_vote_to_author(username, choices, m)

        return HttpResponseRedirect('.')
    else:
        participations = Participation.objects.filter(
            choice__meeting=m.pk).order_by('created')

        months = {}
        days = {}
        total = {} #total participations per choice
        for i, c in enumerate(choices):
            date = c.date
            #find months and colspanning
            month = datetime(date.year, date.month, 1)
            months[month] = 1 + months.get(month, 0)
            
            #find days and colspanning
            day = datetime(date.year, date.month, date.day)
            days[day] = 1 + days.get(day, 0)

            #reset totals
            total[i] = 0
        
        users = [p.user for p in participations]
        users = unique(users)
        
        ##array of participations
        ap = []
        for user in users:
            p = {
                'user': user,
                'choices': []
            }
            u_ps = participations.filter(user=user)
            for i, c in enumerate(choices):
                tmp = u_ps.filter(choice=c).order_by('-created')[0].present
                p['choices'].append(tmp)

                if tmp: total[i] += 1

            ap.append(p)
        
        return render_to_response('meetings/detail.html', {
                'created_now': created_now,
                'meeting': m,
                'choices': choices,
                'months' : sorted(months.iteritems()),
                'days'   : sorted(days.iteritems()),
                'participations' : ap,
                'total'  : total.values(),
            },
            context_instance=RequestContext(request)
        )
