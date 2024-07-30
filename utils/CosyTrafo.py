from typing import Tuple
from math import sqrt, pi, sin, cos, asin, acos, atan2

def deg2rad(val: float) -> float:
    return val / 180 * pi


def rad2deg(val: float) -> float:
    return val / pi * 180

def sin_deg(deg: float) -> float:
    return sin(deg / 180. * pi)

def cos_deg(deg: float) -> float:
    return cos(deg / 180. * pi)


# ----- Basic Mathematical Operations for Polar Coordinates
def add_polar_coordinates(*args: Tuple[float, float], degree: bool = False) -> Tuple[float, float]:
    """
    adds polar coordinates (vectors)
    :param args: arbitrary number of 2-element arrays (vectors), of which the first element represents the distance/
    radius of the polar coordinates and the second element the angle
    :param degree: flag indicating whether the angle of the polar coordinates is provided in degree or not (than radiant
    is assumed). The function also returns the output in degrees if the flag is activated.
    :return:
    """

    # transform to radiant if input is provided in degree
    if degree:
        tuple([el[0], deg2rad(el[1])] for el in args)

    # add polar coordinates by performing in inherit transformation to cartesian coordinates via sin/cos
    arg1 = 0.0
    arg2 = 0.0
    for el in args:
        arg1 += el[0] * cos(el[1])
        arg2 += el[0] * sin(el[1])

    r_add = sqrt(arg1 ** 2 + arg2 ** 2)
    angle_add = atan2(arg2 , arg1)

    # transform to degree if applicable
    if degree:
        angle_add = rad2deg(angle_add)

    return r_add, angle_add


def add_spherical_coordinates(*args: Tuple[float, float, float], degree: bool = False) -> Tuple[float, float, float]:
    xyz = [0.0, 0.0, 0.0]
    for el in args:
        for i, x in enumerate(spherical2cartesian(el, degree=degree)):
            xyz[i] += x
    return cartesian2spherical(tuple(xyz), degree=degree)


# ----- Coordinate Transform
def cylindrical2spherical(vec: Tuple[float, float, float]) -> Tuple[float, float, float]:
    # extract cylindrical coordinates (index cc)
    radius_cc, azimuth_angle_cc, elevation_cc = vec
    # transform to spherical coordinates (index sc)
    distance_sc = sqrt(radius_cc**2 + elevation_cc**2)
    polar_angle_sc = acos(elevation_cc / distance_sc)
    azimuth_angle_sc = azimuth_angle_cc

    return distance_sc, polar_angle_sc, azimuth_angle_sc


def spherical2cylindrical(vec: Tuple[float, float, float]) -> Tuple[float, float, float]:
    # extract spherical coordinates (index sc)
    distance_sc, polar_angle_sc, azimuth_angle_sc = vec
    # transform to cylindrical coordinates (index cc)
    radius_cc = distance_sc * sin(polar_angle_sc)
    azimuth_angle_cc = azimuth_angle_sc
    elevation_cc = distance_sc * cos(polar_angle_sc)

    return radius_cc, azimuth_angle_cc, elevation_cc


def spherical2cartesian(vec: Tuple[float, float, float], degree: bool = False) -> Tuple[float, float, float]:
    # extract spherical coordinates (index sc)
    distance_sc, polar_angle_sc, azimuth_angle_sc = vec
    # transform to radiant if input is provided in degree
    if degree:
        polar_angle_sc = deg2rad(polar_angle_sc)
        azimuth_angle_sc = deg2rad(azimuth_angle_sc)
    assert distance_sc >= 0, f"The radius is supposed to be positive but was {distance_sc}."
    assert (0 <= polar_angle_sc <= pi), f"The polar angle must be in [0, +pi] but was {polar_angle_sc} rad."
    assert (-pi <= azimuth_angle_sc <= pi), f"The azimuth angle must be in [-pi, +pi] but was {azimuth_angle_sc} rad."

    # transform to cartesian coordinates
    x = distance_sc * sin(polar_angle_sc) * cos(azimuth_angle_sc)
    y = distance_sc * sin(polar_angle_sc) * sin(azimuth_angle_sc)
    z = distance_sc * cos(polar_angle_sc)

    return x, y, z


def cartesian2spherical(vec: Tuple[float, float, float], degree: bool = False) -> Tuple[float, float, float]:
    x, y, z = vec
    distance_sc = sqrt(x ** 2 + y ** 2 + z ** 2)
    polar_angle_sc = acos(z / distance_sc) if distance_sc > 0 else 0
    azimuth_angle_sc = atan2(y, x)

    if degree:
        polar_angle_sc = rad2deg(polar_angle_sc)
        azimuth_angle_sc = rad2deg(azimuth_angle_sc)

    return distance_sc, polar_angle_sc, azimuth_angle_sc


def polar2cartesian(vec: Tuple[float, float], degree: bool = False) -> Tuple[float, float]:
    distance_pc = vec[0]
    angle_pc = vec[1]
    # transform to radiant if input is provided in degree
    if degree:
        angle_pc = deg2rad(angle_pc)

    x = distance_pc * cos(angle_pc)
    y = distance_pc * sin(angle_pc)
    return x, y
