"""
WSGI config for ceph project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceph.settings")

application = get_wsgi_application()








def application2(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    import pprint, sys
    print >> sys.stderr, pprint.pformat(environ)
    yield 'Hello World<br>'
    yield 'More content'

