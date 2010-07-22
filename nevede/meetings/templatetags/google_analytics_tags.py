from django import template
from django.conf import settings

register = template.Library()

def google_analytics(s):
    if not (hasattr(settings, 'GA_KEY') and settings.GA_KEY):
        return ''

    return """
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
</script>
<script type="text/javascript">
try {
    var pageTracker = _gat._getTracker("%(gakey)s");
    pageTracker._trackPageview();
} catch(err) {}</script>
""" % { 'gakey': settings.GA_KEY }

register.simple_tag(google_analytics)
