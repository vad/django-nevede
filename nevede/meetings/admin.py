# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Fondazione Bruno Kessler (www.fbk.eu), 2008

from nevede.meetings.models import Meeting, Choice, Participation
from django.contrib import admin
from django import forms

class MeetingModelForm( forms.ModelForm ):
    description     = forms.CharField(widget=forms.Textarea, required = False)
    
    class Meta:
        model = Meeting


class ChoiceInline(admin.TabularInline):
    model = Choice

    
def set_visibility(queryset, private):
    for meeting in queryset:
        meeting.private = private
        meeting.save()

        
class MeetingAdmin(admin.ModelAdmin):
    form            = MeetingModelForm
    list_display    = ('title', 'author_email', 'private', 'created')
    search_fields   = ('title', 'description', 'author_email')
    list_filter     = ('author_email', 'created', 'private')
    date_hierarchy  = 'created'
    inlines         = [ChoiceInline,]
    actions         = ["set_private", "set_public"]
    
    def set_private(self, request, queryset):
        set_visibility(queryset, True)

    def set_public(self, request, queryset):
        set_visibility(queryset, False)

        
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Choice)
admin.site.register(Participation)

