# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Fondazione Bruno Kessler (www.fbk.eu), 2008-2010

from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.contrib.comments.forms import CommentForm
from django.contrib import comments
from django.template.loader import render_to_string
from django.template import RequestContext
from nevede.meetings.models import Meeting, Choice
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class HoursInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return render_to_string('hour_selector.html', {
            'date': name.split('-')[1],
            'name': name,
        })


class MultiDateInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return render_to_string('multi_date_selector.html', {
            'name': name,
        })

class CreoleTextInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return render_to_string('creole_text_input.html', {
                'name': name,
            }
        )

## taken from http://www.djangosnippets.org/snippets/131/
EMPTY_VALUES = (None, '')

class HoneypotWidget(forms.TextInput):
    is_hidden = True
    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not self.attrs.has_key('class'):
            self.attrs['style'] = 'display:none'
    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value

class HoneypotField(forms.Field):
    widget = HoneypotWidget
    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise forms.ValidationError('Anti-spam field changed in value.')


class CreateMeetingForm_1(forms.Form):
    title = forms.CharField(max_length=200, error_messages={'required':
                'The field below is required'})
    description = forms.CharField(widget=CreoleTextInput, max_length=2000,
        required=False, label="Description (optional)",
        help_text="<a class='field-help' href='http://www.wikicreole.org/"+
        "attach/CheatSheet/creole_cheat_sheet.html' target='_blank'>"+
        "Syntax help</a>")
    author_email = forms.EmailField(label="Your email (optional)",
                                    required=False)
    trustme = HoneypotField()
    dates = forms.CharField(widget=MultiDateInput, max_length=200,
                            error_messages={'required':
                                            'The field below is required'})
    private = forms.BooleanField(required=False)



class CreateMeetingForm_2(forms.Form):
    def __init__(self, *args, **kwargs):
        from datetime import datetime

        super(CreateMeetingForm_2, self).__init__(*args, **kwargs)
        
        #loop over days
        for field in kwargs.get('initial').get('hours'):
            date = datetime.utcfromtimestamp(int(field[0:-3]))
            self.fields[field] =  forms.CharField(
                widget=HoursInput, max_length=1000,
                required=False, label=date.strftime('%Y-%m-%d'))


class CreateMeetingWizard(FormWizard):
    def done(self, request, form_list):
        from django.utils.simplejson.decoder import JSONDecoder
        from datetime import datetime
        from nevede.meetings.email import send_created_meeting_to_author

        init_data = {}
        for attr in 'title,description,private,author_email'.split(','):
            init_data[attr] = form_list[0].cleaned_data[attr]

        m = Meeting(**init_data)
        m.save()
        
        if init_data['author_email']:
            send_created_meeting_to_author(m)

        for k,v in form_list[1].cleaned_data.iteritems():
            ## skip day k if it hasn't choices
            if not v:
                continue
            
            date = datetime.utcfromtimestamp(int(k[0:-3]))
            for t in JSONDecoder().decode(v):
                if not t:
                    continue
            
                c = Choice(meeting=m, text=t, date=date)
                c.save()
                
            request.session['meeting_created'] = True

        return HttpResponseRedirect(reverse('nevede.meetings.views.detail',
            args=(m.hidden_id,))) # Redirect after POST
   
    def parse_params(self, request, *args, **kwargs):
        """
        pass parameters between first and second form
        """
        current_step = self.determine_step(request, *args, **kwargs)

        if request.method == 'POST' and current_step == 0:
            form = self.get_form(current_step, request.POST)
            if form.is_valid():
                self.initial[(current_step + 1)] = {
                    'hours': form.cleaned_data['dates'].split(','),
                }

    def get_template(self, step):
        return 'meetings/wizard_%s.html' % step

## COMMENTS
class NevedeCommentForm(CommentForm):
    next = forms.CharField(widget=forms.HiddenInput, max_length=50)

def returnnevedecommentform():
    return NevedeCommentForm

comments.get_form = returnnevedecommentform
