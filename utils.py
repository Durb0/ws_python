import math
import geopy.distance
from typing import List, Tuple
import requests


def get_shortest_path(start: Tuple[float, float], end: Tuple[float, float], max_distance: float, charging_stations: List[Tuple[float, float]]) \
        -> List[Tuple[float, float]]:
    def get_center(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> Tuple[float, float]:
        return (point_a[0] + point_b[0]) / 2, (point_a[1] + point_b[1]) / 2

    def get_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
        return geopy.distance.distance(point_a, point_b).km

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

    res_list = [start]

    while res_list[-1] != end:
        print(res_list)
        if get_distance(res_list[-1], end) < max_distance:
            res_list.append(end)
            print("don't need to charge")
            break
        borns_around = get_borns_around(res_list[-1])
        if len(borns_around) == 0:
            res_list.append(end)
            print("no borns around")
            break
        shortest_coord = get_shortest_coord(end, borns_around)
        if shortest_coord is None:
            res_list.append(end)
            print("no shortest coord")
            break
        if shortest_coord == res_list[-1]:
            res_list.append(end)
            print("shortest coord is the same as the last one")
            break
        res_list.append(shortest_coord)

    return res_list
