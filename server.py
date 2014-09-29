#!/usr/bin/python
import time
import gevent
import gevent.monkey
import gevent.server
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
import logging
import logging.config
import yaml
import sys
import os
import subprocess

logger = logging.getLogger("system")

def application(env, start_response):
    path = env['PATH_INFO']
    qs = env['QUERY_STRING']
    logger.info(path + "?" + qs)

    start_response('204 No Content', [])
    return []

class LogServer(gevent.server.DatagramServer):
    def handle(self, data, address):
        logger.info(data)


def upload(filename, bucket, callback):
    while True:
        subprocess.Popen(["python", callback, filename, bucket])
        gevent.sleep(5)

def start(bucket, type="TCP", port=8080, filename="request.log", when="H", callback="upload.py"):
    config = yaml.load(open('conf.yaml', 'r').read().format(**{
        "filename": filename,
        "when": when
    }))
    logging.config.dictConfig(config)

    print('Serving %s on %s...' % (type, port ))
    gevent.spawn(upload, filename, bucket, callback)

    if type == "TCP":
        WSGIServer(('', port), application).serve_forever()
    else:
        LogServer(":%s" % port).serve_forever()


if __name__ == '__main__':
   import clime; clime.start()
    # start('tagtoo_rtb_log', type="UDP")

