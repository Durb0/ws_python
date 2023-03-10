import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer

import utils


class TrajectService(ServiceBase):

    @rpc(Float, Float, Float, Float, Integer, _returns=Iterable(Iterable(Float)))
    def calculate_traject(self, start_lng, start_lat, finish_lng, finish_lat, range):
        self.transport.resp_headers['Access-Control-Allow-Origin'] = '*'
        print('calculate_traject(%r, %r, %r, %r)' % (start_lng, start_lat, finish_lng, finish_lat))
        # calculate the distance between the two points, return the distance in km
        res = utils.get_shortest_path((start_lat, start_lng), (finish_lat, finish_lng), range)
        print(res)
        return res
