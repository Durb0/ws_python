import math
import geopy.distance
from typing import List, Tuple
import requests


def get_shortest_path(start: Tuple[float, float], end: Tuple[float, float], max_distance: float) \
        -> List[Tuple[float, float]]:

    def get_charging_stations_around(center: Tuple[float, float]) -> List[Tuple[float, float]]:
        apiUrl = 'https://odre.opendatasoft.com/api/records/1.0/search/'
        params = {
            'dataset': 'bornes-irve',
            'rows': 5000,
            'geofilter.distance': '%s,%s,%s' % (center[0], center[1], max_distance*1000)
        }
        response = requests.get(apiUrl, params=params, timeout=30000)
        data = response.json()
        records = data['records']
        coords = []
        for record in records:
            coords.append((record['geometry']['coordinates'][1], record['geometry']['coordinates'][0]))
        return coords

    def get_shortest_coord(center: Tuple[float, float], coords: List[Tuple[float, float]]) -> Tuple[float, float]:
        shortest_distance = math.inf
        shortest_coord = None
        for coord in coords:
            distance = geopy.distance.distance(center, coord).km
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_coord = coord
        return shortest_coord

    def get_coords_around(center: Tuple[float, float], coords: List[Tuple[float, float]]) -> List[
        Tuple[float, float]]:
        coords_around = []
        for coord in coords:
            distance = geopy.distance.distance(center, coord).km
            if distance < max_distance:
                coords_around.append(coord)
        return coords_around

    list = []
    # il faut faire une recursivité pour trouver le chemin le plus court
    # si la distance entre le point de départ et le point d'arrivée est inférieur à la distance max
    # alors on retourne le point d'arrivée
    # sinon on cherche l'ensemble des points de charge autour du point de départ
    # on cherche le point de charge le plus proche du point d'arrivée
    # on rappelle la fonction avec le point de charge le plus proche comme point de départ
    # et le point d'arrivée comme point d'arrivée

    list.append(start)
    distance = geopy.distance.distance(start, end).km
    if distance < max_distance:
        list.append(end)
        return list
    else:
        charging_stations = get_charging_stations_around(start)
        coords_around = get_coords_around(start, charging_stations)
        # si il n'y a pas de point de charge autour du point de départ
        # alors on retourne le point d'arrivée
        if len(coords_around) == 0:
            list.append(end)
            return list
        shortest_coord = get_shortest_coord(end, coords_around)
        # si il n'y a pas de point de charge autour du point de départ
        # alors on retourne le point d'arrivée
        list.extend(get_shortest_path(shortest_coord, end, max_distance))
        return list
