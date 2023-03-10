import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer

import utils


class CorsService(ServiceBase):
    origin = '*'


def _on_method_return_object(ctx):
    ctx.transport.resp_headers['Access-Control-Allow-Origin'] = \
        ctx.descriptor.service_class.origin


CorsService.event_manager.add_listener('method_return_object', _on_method_return_object)


class TrajectService(CorsService):

    @rpc(Float, Float, Float, Float, Integer, _returns=Iterable(Iterable(Float)))
    def calculate_traject(ctx, start_lng, start_lat, finish_lng, finish_lat, autonomy):
        print('calculate_traject(%r, %r, %r, %r)' % (start_lng, start_lat, finish_lng, finish_lat))
        return utils.get_shortest_path((start_lng, start_lat), (finish_lng, finish_lat), autonomy)
