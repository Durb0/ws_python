from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from api.traject_service import TrajectService

if __name__ == "__main__":
    # Create a new instance of the app
    application = Application([TrajectService], 'info.802.traject.soap',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_application = WsgiApplication(application)
    # Run the app
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, wsgi_application)
    server.serve_forever()