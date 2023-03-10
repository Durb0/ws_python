from wsgiref.simple_server import make_server
from application import wsgi_application

server = make_server('localhost', 8000, wsgi_application)
server.serve_forever()