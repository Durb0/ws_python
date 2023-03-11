import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer

import utils


class TrajectService(ServiceBase):
    # Spécifie le nom de l'opération SOAP
    origin = '*'

    @rpc(Float, Float, Float, Float, Integer, _returns=Iterable(Iterable(Float)))
    def calculate_traject(ctx, start_lng, start_lat, finish_lng, finish_lat, autonomy):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        print(f'calculate_traject({start_lng}, {start_lat}, {finish_lng}, {finish_lat})')
        return utils.get_shortest_path((start_lng, start_lat), (finish_lng, finish_lat), autonomy)

