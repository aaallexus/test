# test.py
import sys
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World-------!!!!!!_-----___-_--____-"] # python2
