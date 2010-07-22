# LICENSE: AGPL 3.0
# Author: Name: Davide, Surname: Setti, email: NAME.SURNAME@gmail.com
# Copyright: Fondazione Bruno Kessler (www.fbk.eu), 2008-2010

from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import loader, Context

def send_created_meeting_to_author(m):
    """
    Send a confirmation email to the author of the meeting passed as parameter to this function.
    
    Returns True if succeed.
    """
    if not settings.EMAIL:
        return False
    
    current_site = Site.objects.get_current()

    sender = 'noreply@'+current_site.domain
    t = loader.get_template('meetings/email/creation_notification_email.txt')
    c = Context({'meeting': m,
                 'site': current_site})
    message = t.render(c)

    send_mail('[nevede] A new meeting "%s" has been created' % (m.title,),
        message, sender, [m.author_email])
    
    return True


def send_vote_to_author(username, choices, m):
    if not settings.EMAIL:
        return False
        
    current_site = Site.objects.get_current()

    sender = 'noreply@'+current_site.domain
    t = loader.get_template('meetings/email/vote_notification_email.txt')
    c = Context({'user': username,
                 'meeting': m,
                 'site': current_site})
    message = t.render(c)

    send_mail('[nevede] A new vote has been submitted for "%s"' % (m.title,),
        message, sender, [m.author_email])
    
    return True


def send_comment_to_author(comment, m):
    if not settings.EMAIL:
        return False
    username = comment.user_name
    
    current_site = Site.objects.get_current()

    sender = 'noreply@'+current_site.domain
    c = Context({'user': username,
                 'comment': comment,
                 'meeting': m,
                 'site': current_site})
    message = loader.get_template('meetings/email/vote_notification_email.txt'
                                  ).render(c)
    
    send_mail('[nevede] A new comment has been posted for "%s"' % (m.title,),
        message, sender, [m.author_email])

    return True