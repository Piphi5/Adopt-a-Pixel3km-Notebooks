import math


def get_latlon_spacing_constants(grid_distance, latitude):
    # Calculate grid constants
    r_earth = 6.371 * 10 ** 6

    # See Theoretical Basis for the derivations
    latitude_const = (
        360 / math.pi * math.asin((math.sin(grid_distance / (2 * r_earth))))
    )
    longitude_const = (
        360
        / math.pi
        * math.asin(
            math.sin(grid_distance / (2 * r_earth)) / math.cos(latitude * math.pi / 180)
        )
    )

    return latitude_const, longitude_const
