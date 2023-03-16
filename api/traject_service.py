import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer, Application, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import utils
import ast

class TrajectService(ServiceBase):
    # Spécifie le nom de l'opération SOAP
    origin = '*'

    @rpc(Float, Float, Float, Float, Integer,String , _returns=Iterable(Iterable(Float)))
    def calculate_traject(ctx, start_lat, start_lng, finish_lat, finish_lng, autonomy, charging_stations):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        #convert charging stations (string) to list of tuples
        charging_stations = ast.literal_eval(charging_stations)
        charging_stations = [(float(x), float(y)) for x, y in charging_stations]

        return utils.get_shortest_path((start_lat, start_lng), (finish_lat, finish_lng), autonomy, charging_stations)


application = Application([TrajectService], 'info.802.traject.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())


wsgi_application = WsgiApplication(application)
app = wsgi_application
