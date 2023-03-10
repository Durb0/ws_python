from wsgiref.simple_server import make_server
from application import wsgi_application

app = wsgi_application()