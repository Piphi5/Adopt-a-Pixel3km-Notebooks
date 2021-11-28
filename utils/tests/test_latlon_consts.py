import pytest

from haversine import haversine, Unit
from utils.code.grid_constants import get_latlon_constants


test_points = [
    (30.601389, -96.314445, 500),
    (27.798244, -82.798462, 100),
    (-17.221666, -46.875000, 10),
    (-15.793889, -47.882778, 500),
    (-22.752754, -42.864876, 50),
    (34.383331, 132.449997, 10),
    (34.672314, 135.484802, 100),
    (42.349998, 14.166667, 500),
    (41.683334, 15.383333, 150),
    (-16.442181, 46.543468, 100),
]


@pytest.mark.parametrize("lat, lon, distance", test_points)
def test_latlon_consts(lat, lon, distance):
    lat_const, lon_const = get_latlon_constants(distance, lat)
    point = (lat, lon)
    west_point = (lat + lat_const, lon)
    north_point = (lat, lon + lon_const)
    assert haversine(point, west_point, unit=Unit.METERS) == pytest.approx(
        distance, 0.001
    )
    assert haversine(point, north_point, unit=Unit.METERS) == pytest.approx(
        distance, 0.001
    )
