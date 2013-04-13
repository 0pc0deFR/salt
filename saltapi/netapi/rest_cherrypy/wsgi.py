#!/usr/bin/env python
'''
Deployment
==========

The ``rest_cherrypy`` netapi module is a standard Python WSGI app. It can be
deployed one of two ways.

:program:`salt-api` using the CherryPy server
---------------------------------------------

The default configuration is to run this module using :program:`salt-api` to
start the Python-based CherryPy server. This server is lightweight,
multi-threaded, encrypted with SSL, and should be considered production-ready.

Using a WSGI-compliant web server
---------------------------------

This module may be deplayed on any WSGI-compliant server such as Apache with
mod_wsgi or Nginx with FastCGI, to name just two (there are many).

An example Apache virtual host configuration::

    <VirtualHost *:80>
        ServerName example.com
        ServerAlias *.example.com

        ServerAdmin webmaster@example.com

        LogLevel warn
        ErrorLog /var/www/example.com/logs/error.log
        CustomLog /var/www/example.com/logs/access.log combined

        DocumentRoot /var/www/example.com/htdocs

        WSGIScriptAlias / /path/to/saltapi/netapi/rest_cherrypy/wsgi.py
    </VirtualHost>

'''
# pylint: disable=C0103

import cherrypy

from . import app

def bootstrap_app():
    '''
    Grab the opts dict of the master config by trying to import Salt
    '''
    import salt.client
    opts = salt.client.LocalClient().opts
    return app.get_app(opts)

def get_application(*args):
    '''
    Returns a WSGI application function. If you supply the WSGI app and config
    it will use that, otherwise it will try to obtain them from a local Salt
    installation
    '''
    opts_tuple = args

    def wsgi_app(environ, start_response):
        root, _, conf = opts_tuple or bootstrap_app()

        cherrypy.tree.mount(root, '/', conf)
        return cherrypy.tree(environ, start_response)

    return wsgi_app

application = get_application()
