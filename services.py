import geopy.distance
from spyne import rpc, ServiceBase, Float, Iterable, Integer

import utils


class CorsService(ServiceBase):
    # Définit l'origine autorisée pour les demandes cross-domain
    origin = '*'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajoute un gestionnaire d'événements pour l'événement method_return_object
        self.event_manager.add_listener('method_return_object', self._on_method_return_object)

    def _on_method_return_object(self, ctx):
        # Ajoute l'en-tête Access-Control-Allow-Origin avec l'origine autorisée
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = self.origin


class TrajectService(CorsService):
    # Spécifie le nom de l'opération SOAP
    __tns__ = 'spyne.examples.hello.soap'

    @rpc(Float, Float, Float, Float, Integer, _returns=Iterable(Iterable(Float)))
    def calculate_traject(ctx, start_lng, start_lat, finish_lng, finish_lat, autonomy):
        print(f'calculate_traject({start_lng}, {start_lat}, {finish_lng}, {finish_lat})')
        return utils.get_shortest_path((start_lng, start_lat), (finish_lng, finish_lat), autonomy)

