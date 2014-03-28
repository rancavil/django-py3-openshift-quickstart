#!/usr/bin/env python
import os

#
# Below for testing only
#
if __name__ == '__main__':
    ip   = 'localhost'
    port = 8051
    zapp = imp.load_source('application', 'wsgi/application')

    from wsgiref.simple_server import make_server
    httpd = make_server(ip, port, zapp.application)
    httpd.serve_forever()
