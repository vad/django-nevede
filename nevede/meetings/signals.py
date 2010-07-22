from django.conf import settings
from django.contrib.comments import signals
from django.contrib import comments
from nevede.meetings.email import send_comment_to_author

def comment_send_email_to_author(sender, comment, request, **kwargs):
    if not settings.EMAIL:
        return
    
    meeting = comment.content_object
    author_email = meeting.author_email
    if not author_email:
        return
    
    send_comment_to_author(comment, meeting)
        

signals.comment_was_posted.connect(comment_send_email_to_author,
                                   sender=comments.get_model())

