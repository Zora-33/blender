
from CosyTrafo import *


from typing import Union, List, Tuple


def rotate_roll(vec: Tuple[Union[int, float]], angle_deg: float) -> Tuple[Union[int, float]]:
    """
    | 1    0          0      |
    | 0 cos(roll) -sin(roll) |
    | 0 sin(roll)  cos(roll) |
    """
    cosc = round(cos_deg(angle_deg), 15)
    sinc = round(sin_deg(angle_deg), 15)
    rotation_matrix = ((1.0, 0.0, 0.0),
                       (0.0, cosc, -sinc),
                       (0.0, sinc, cosc))
    # apply rot matrix
    return mat_multiply(rotation_matrix, vec)

def rotate_pitch(vec: Tuple[Union[int, float]], angle_deg: float) -> Tuple[Union[int, float]]:
    """
    | cos(pitch) 0 -sin(pitch) |
    |     0      1      0      |
    | sin(pitch) 0  cos(pitch) |
    """
    cosc = round(cos_deg(angle_deg), 15)
    sinc = round(sin_deg(angle_deg), 15)
    rotation_matrix = ((cosc, 0.0, -sinc),
                       (0.0, 1.0, 0.0),
                       (sinc, 0.0, cosc))
    # apply rot matrix
    return mat_multiply(rotation_matrix, vec)

def rotate_yaw(vec: Tuple[Union[int, float]], angle_deg: float) -> Tuple[Union[int, float]]:
    """
    | cos(yaw) -sin(yaw) 0 |
    | sin(yaw)  cos(yaw) 0 |
    |    0         0     1 |
    """
    cosc = round(cos_deg(angle_deg), 15)
    sinc = round(sin_deg(angle_deg), 15)
    rotation_matrix = ((cosc, -sinc, 0.0),
                       (sinc, cosc, 0.0),
                       (0.0, 0.0, 1.0))
    # apply rot matrix
    return mat_multiply(rotation_matrix, vec)