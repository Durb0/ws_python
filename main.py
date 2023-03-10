from wsgiref.simple_server import make_server
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from services import TrajectService

application = Application([TrajectService], 'spyne.examples.hello.http',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
app = wsgi_application
