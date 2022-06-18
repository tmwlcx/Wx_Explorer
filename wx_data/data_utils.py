# data_utils.py
from math import sin, cos, sqrt, radians, asin
def haversine_distance(point_A, point_B):
    """
    Function to return the orthodromic distance between 2 points in km

    Args: 
        point_A: [list] - a list containing [latitude, longitude] decimal coordinates of the first point
        point_B: [list] - a list containing [latitude, longitude] decimal coordinates of the second point
    
    Returns:
        distance (km)
    """
    assert type(point_A) == list, "Coordinates for point_A must be a list of [lat, long]"
    assert type(point_B) == list, "Coordinates for point_B must be a list of [lat, long]"

    r_earth = 6371 # radius of the earth in km

    [lat_A, lon_A], [lat_B, lon_B] = point_A, point_B
    lat_A, lon_A, lat_B, lon_B = map(radians, [lat_A, lon_A, lat_B, lon_B])

    d_lon = lon_B - lon_A
    d_lat = lat_B - lat_A

    a = sin(d_lat/2)**2 + cos(lat_A) * cos(lat_B) * sin(d_lon/2) ** 2
    c = 2 * asin(sqrt(a))
    d = c * r_earth
    return d