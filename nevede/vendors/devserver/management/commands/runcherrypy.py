from django.core.management.base import BaseCommand, CommandError
from django.core.handlers.wsgi import WSGIHandler

import django.contrib.admin

from cherrypy.wsgiserver import CherryPyWSGIServer, WSGIPathInfoDispatcher
from nevede.vendors.devserver.mediahandler import *
import os.path

from optparse import OptionParser, make_option

class Command(BaseCommand):

    help = "Starts a WSGI Web server based on Cherrypy."
    args = '[optional port number, or ipaddr:port]'
    
    def handle(self, addrport='', *args, **options):
        if args:
            raise CommandError('Usage is runcherrypy %s' % self.args)
        if not addrport:
            addr = ''
            port = '8000'
        else:
            try:
                addr, port = addrport.split(':')
            except ValueError:
                addr, port = '', addrport
        if not addr:
            addr = '127.0.0.1'

        try:
            port = int(port)
        except ValueError:
            raise CommandError("%r is not a valid port number." % port)
        
        app = WSGIHandler()

        path = { '/': app,
                 settings.MEDIA_URL: MediaHandler(settings.MEDIA_ROOT),
                 settings.ADMIN_MEDIA_PREFIX:
                     MediaHandler(
                         os.path.join(django.contrib.admin.__path__[0],
                                       'media')
                         )
               }
        dispatcher = WSGIPathInfoDispatcher(path)
        server = CherryPyWSGIServer((addr, port), dispatcher)

        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()

    def create_parser(self, prog, subcommand):
        """
        Create and return the ``OptionParser`` which will be used to
        parse the arguments to this command.
        """
        return OptionParser( prog=prog,
                             usage=self.usage(subcommand),
                             version=self.get_version(),
                             option_list=self.option_list,
                             conflict_handler="resolve" )
