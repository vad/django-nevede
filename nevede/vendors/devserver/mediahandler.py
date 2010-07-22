import os, stat, mimetypes
import django
from django.utils.http import http_date
from django.conf import settings

class MediaHandler( object ):

    def __init__( self, media_root ):
        self.media_root = media_root

    def __call__( self, environ, start_response ):

        def done( status, headers, output ):
            start_response( status, headers.items() )
            return output

        path_info = environ['PATH_INFO']
        path_info = path_info.lstrip('/')

        file_path = os.path.join( self.media_root, path_info )

        if not os.path.exists( file_path ):
            status = '404 NOT FOUND'
            headers = {'Content-type': 'text/plain'}
            output = ['Page not found: %s' % file_path]
            return done( status, headers, output )

        try:
            fp = open( file_path, 'rb' )
        except IOError:
            status = '401 UNAUTHORIZED'
            headers = {'Content-type': 'text/plain'}
            output = ['Permission denied: %s' % file_path]
            return done( status, headers, output )
        
        # This is a very simple implementation of conditional GET with
        # the Last-Modified header. It makes media files a bit speedier
        # because the files are only read off disk for the first request
        # (assuming the browser/client supports conditional GET).

        mtime = http_date( os.stat(file_path)[stat.ST_MTIME] )
        headers = {'Last-Modified': mtime}
        if environ.get('HTTP_IF_MODIFIED_SINCE', None) == mtime:
            status = '304 NOT MODIFIED'
            output = []
        else:
            status = '200 OK'
            mime_type = mimetypes.guess_type(file_path)[0]
            if mime_type:
                headers['Content-Type'] = mime_type
            output = [fp.read()]
            fp.close()

        return done( status, headers, output )
