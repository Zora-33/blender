import blenderproc as bproc
import math
import random
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector, Matrix
from typing import Tuple, Union, List, Dict
from numpy.typing import NDArray


def create_perpendicular_vector(
    v: Union[List[float], Tuple[float, float, float], NDArray[np.float64]]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """find two simple vector which perpendicular to v"""
    x, y, z = v
    if x == 0 and y == 0:
        return np.asarray((1, 0, 0)), np.asarray((0, 1, 0))
    else:
        perp1 = np.array([-y, x, 0])
        perp1 = perp1 / np.linalg.norm(perp1)

        perp2 = np.cross(v, perp1)
        perp2 = perp2 / np.linalg.norm(perp2)

        return perp1, perp2


def look_at(
    camera_location: Union[
        List[float], Tuple[float, float, float], NDArray[np.float64]
    ],
    target_location: Union[
        List[float], Tuple[float, float, float], NDArray[np.float64]
    ],
) -> Tuple[float, float, float]:
    """let the camera look at the object"""
    direction = Vector(target_location) - Vector(camera_location)
    # the rotation needed to align the default forward direction (-Z) with the computed direction vector
    # the direction of Y does not change during rotation
    return direction.to_track_quat("-Z", "Y").to_euler()


def random_point_on_unit_circle() -> Tuple[float, float]:
    """return the unit(x,y) in circle"""
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)


def change_to_spherical(theta: float, phi: float, radius: float) -> Tuple[float, float, float]:
    """Transform spherical to Cartesian"""
    camera_x = radius * math.sin(theta) * math.cos(phi)
    camera_y = radius * math.sin(theta) * math.sin(phi)
    camera_z = radius * math.cos(theta)
    return camera_x, camera_y, camera_z


if __name__ == "__main__":
    bproc.init()

    # Create a simple object:

    # Object position as coordinate origin
    monkey = bproc.object.create_primitive("MONKEY")
    monkey.set_location([0, 0, 0])
    monkey.set_rotation_euler([0, 0, 0])
    object_position = np.array([0, 0, 0])
    # The r will change in 10%. 
    R = random.uniform(4.5, 5.5)

    theta = random.uniform(0, math.pi)
    phi = random.uniform(0, 2 * math.pi)

    camera_position = change_to_spherical(theta, phi, r)
    rotation_euler = look_at(camera_position, object_position)
    cam_pose = bproc.math.build_transformation_mat(camera_position, rotation_euler)

    bproc.camera.add_camera_pose(cam_pose)

    # Light position will be in solar coordinate from a random distribution

    # Create a point light next to it

    cam_pose = bproc.math.build_transformation_mat(
        [0, -5, 0],
        [np.pi / 2, 0, 0]
    )
    bproc.camera.add_camera_pose(cam_pose)

    # get two simple vectors which perpendicular to v
    perp1, perp2 = create_perpendicular_vector(camera_position)

    circle_x, circle_y = random_point_on_unit_circle()

    # light position
    light_position = camera_position + circle_x * perp1 + circle_y * perp2

    light = bproc.types.Light()
    light.set_location(light_position.tolist())
    light.set_type("POINT")
    light.set_energy(500)

    bproc.renderer.set_output_format(file_format="PNG")
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.cycles.samples = 100

    # rendering
    data = bproc.renderer.render()
    print(f"Type {type(data)}")

    output_dir = Path("output")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    bproc.writer.write_hdf5(output_dir.as_posix(), data)

