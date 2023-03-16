import math
import geopy.distance
from typing import List, Tuple
import requests


def get_shortest_path(start: Tuple[float, float], end: Tuple[float, float], max_distance: float) \
        -> List[Tuple[float, float]]:
    def get_center(pointA: Tuple[float, float], pointB: Tuple[float, float]) -> Tuple[float, float]:
        return ((pointA[0] + pointB[0]) / 2, (pointA[1] + pointB[1]) / 2)

    def get_distance(pointA: Tuple[float, float], pointB: Tuple[float, float]) -> float:
        return geopy.distance.distance(pointA, pointB).km

    def get_charging_stations_around(center: Tuple[float, float], radius) -> List[Tuple[float, float]]:
        apiUrl = 'https://odre.opendatasoft.com/api/records/1.0/search/'
        params = {
            'dataset': 'bornes-irve',
            'rows': 5000,
            'geofilter.distance': '%s,%s,%s' % (center[0], center[1], radius * 1000)
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

    def get_borns_around(center: Tuple[float, float]) -> List[
        Tuple[float, float]]:
        coords_around = []
        for coord in charging_stations:
            distance = geopy.distance.distance(center, coord).km
            if distance < max_distance:
                coords_around.append(coord)
        return coords_around

    if get_distance(start, end) < max_distance:
        return [start, end]

    charging_stations = get_charging_stations_around(get_center(start, end), get_distance(start, end) / 2)

    res_list = [start]

    while res_list[-1] != end:
        print(res_list)
        if get_distance(res_list[-1], end) < max_distance:
            res_list.append(end)
            break
        borns_around = get_borns_around(res_list[-1])
        if len(borns_around) == 0:
            res_list.append(end)
            break
        shortest_coord = get_shortest_coord(end, borns_around)
        if shortest_coord is None:
            res_list.append(end)
            break
        if shortest_coord == res_list[-1]:
            res_list.append(end)
            break
        res_list.append(shortest_coord)

    return res_list
