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
        for i, x in enumerate(spherical_to_cartesian(*el, degree=degree)):
            xyz[i] += x
    return cartesian_to_spherical(*tuple(xyz), degree=degree)


# ----- Coordinate Transform
def cylindrical_to_spherical(
        r: float,
        azimuth_angle: float,
        h: float
) -> Tuple[float, float, float]:
    """transforms cylindrical coordinates to spherical coordinates"""
    # transform to spherical coordinates (index sc)
    distance_sc = sqrt(r**2 + h**2)
    polar_angle_sc = acos(h / distance_sc)

    return distance_sc, polar_angle_sc, azimuth_angle


def spherical_to_cylindrical(
        r: float,
        polar_angle: float,
        azimuth_angle: float
) -> Tuple[float, float, float]:
    """transforms spherical coordinates to cylindrical coordinates"""

    # transform to cylindrical coordinates (index cc)
    radius_cc = r * sin(polar_angle)
    azimuth_angle_cc = azimuth_angle
    elevation_cc = r * cos(polar_angle)

    return radius_cc, azimuth_angle_cc, elevation_cc


def spherical_to_cartesian(
        r: float,
        polar_angle: float,
        azimuth_angle: float,
        degree: bool = False
) -> Tuple[float, float, float]:
    """transforms spherical coordinates to cartesian coordinates"""

    # transform to radiant if input is provided in degree
    if degree:
        polar_angle = deg2rad(polar_angle)
        azimuth_angle = deg2rad(azimuth_angle)

    assert r >= 0, f"The radius is supposed to be positive but was {r}."
    assert (0 <= polar_angle <= pi), f"The polar angle must be in [0, +pi] but was {polar_angle} rad."
    assert (-pi <= azimuth_angle <= pi), f"The azimuth angle must be in [-pi, +pi] but was {azimuth_angle} rad."

    # transform to cartesian coordinates
    x = r * sin(polar_angle) * cos(azimuth_angle)
    y = r * sin(polar_angle) * sin(azimuth_angle)
    z = r * cos(polar_angle)

    return x, y, z


def cartesian_to_spherical(
        x: float,
        y: float,
        z: float,
        degree: bool = False
) -> Tuple[float, float, float]:
    """transforms cartesian coordinates to spherical coordinates"""

    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    polar_angle = acos(z / r) if r > 0 else 0
    azimuth_angle = atan2(y, x)

    if degree:
        polar_angle = rad2deg(polar_angle)
        azimuth_angle = rad2deg(azimuth_angle)

    return r, polar_angle, azimuth_angle


def polar_to_cartesian(
        r: float,
        phi: float,
        degree: bool = False
) -> Tuple[float, float]:
    """transforms polar coordinates to 2D cartesian coordinates"""

    # transform to radiant if input is provided in degree
    if degree:
        phi = deg2rad(phi)

    x = r * cos(phi)
    y = r * sin(phi)
    return x, y


def cartesian_to_cylindrical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """transforms from cartesian coordinates to cylindrical coordinates"""
    r = sqrt(x**2 + y**2)
    theta = atan2(y, x)

    return r, theta, z


def cylindrical_to_cartesian(r: float, theta: float, z: float) -> Tuple[float, float, float]:
    """transforms from cylindrical coordinates to cartesian coordinates"""
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y, z
