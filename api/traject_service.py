import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer, Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import utils


class TrajectService(ServiceBase):
    # Spécifie le nom de l'opération SOAP
    origin = '*'

    @rpc(Float, Float, Float, Float, Integer, _returns=Iterable(Iterable(Float)))
    def calculate_traject(ctx, start_lng, start_lat, finish_lng, finish_lat, autonomy):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        return utils.get_shortest_path((start_lat, start_lng), (finish_lat, finish_lng), autonomy)


application = Application([TrajectService], 'info.802.traject.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
app = wsgi_application
