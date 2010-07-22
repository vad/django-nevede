from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

def creole(value):
    try:
        from creoleparser import text2html
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% creole %} filter: The Python creoleparser library isn't installed."
        return force_unicode(value)
    else:
        return mark_safe(force_unicode(text2html(force_unicode(smart_str(value)))))
creole.is_safe = True

register.filter(creole)
