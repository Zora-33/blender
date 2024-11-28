import blenderproc as bproc
import bpy
import math
import random
import numpy as np
import warnings
import os
from blenderproc.scripts.saveAsImg import save_array_as_image
from pathlib import Path
from numpy.typing import NDArray
from mathutils import Vector, Matrix
from typing import Tuple, Union, List, Dict




def choose_and_set_light(
        position: Union[List[float], Tuple[float, float, float], NDArray[np.float64]],
        energy: int,
        p: float
) -> None:
    """Selection of a point or bar light source from a given position and energy according to the p-value"""
    assert (0 <= p <= 1), ValueError("Input 'p' must be between 0 and 1.")
    light = bproc.types.Light()
    if random.random() < p:
        # create bar light
        light.set_type("AREA")
    else:
        # create point light if greater the user-defined percentage
        light.set_type("POINT")
    light.set_energy(energy)
    light.set_location(position.tolist())


def create_perpendicular_vector(
    v: Union[List[float], Tuple[float, float, float], NDArray[np.float64]]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Find two simple vector which perpendicular to v"""
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
    camera_location: Union[List[float], Tuple[float, float, float], NDArray[np.float64]],
    target_location: Union[List[float], Tuple[float, float, float], NDArray[np.float64]],
) -> Tuple[float, float, float]:
    """Let the camera look at the object"""
    direction = Vector(target_location) - Vector(camera_location)
    # the rotation needed to align the default forward direction (-Z) with the computed direction vector
    # the direction of Y does not change during rotation
    return direction.to_track_quat("-Z", "Y").to_euler()

def add_texture(image_path: Union[str, Path], obj: object):
    # check if obj object format
    if not isinstance(obj, bproc.types.MeshObject):
        raise ValueError(
            "The provided object is not a valid BlenderProc MeshObject. Make sure to pass a correct object.")
    image_path = Path(image_path).absolute()
    # create material
    material = bproc.material.create("stl_material")
    # load image
    image = bpy.data.images.load(filepath=str(image_path))
    # Sets the material's Base Color to Texture
    material.set_principled_shader_value("Base Color", image)
    obj.replace_materials(material)


def color2rgb(color: Union[str, Tuple[int, int, int], List[int]]) -> Tuple[float, float, float]:
    """
    Parses a user-defined color string and converts it to an RGB tuple that Blender can use.
    """
    # judgment the formate 'R,G,B' or '#RRGGBB'

    if isinstance(color, str):
        if re.match(r"^#([0-9A-Fa-f]{6})$", color):
            r, g, b = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
        else:
            # convert to tuple
            try:
                r, g, b = ast.literal_eval(color)
            except Exception as ex:
                r, g, b = 255, 255, 255
                ValueError("Color must be in the format 'R,G,B' or '#RRGGBB'.")
    else:
        r, g, b = color

    # normalize
    r /= 255.0
    g /= 255.0
    b /= 255.0
    return r, g, b

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
    #If the obj file doesn't have uv coordinates, you need to create them yourself,
    # otherwise the added texture will only show the base colour with no texture.
    objpath = "C:/Users/TianXue/Downloads/new.obj"
    image_dir = "C:/Users/TianXue/PycharmProjects/BlenderImageRendering/sample_texture.jpg"
    output_dir = Path("C:/Users/TianXue/PycharmProjects/BlenderImageRendering")
    n_images = 4
    max_theta = np.pi
    max_phi = np.pi
    light_percentage = random.uniform(0, 1)
    background_color = (255, 255, 255)

    distance_object_camera: Tuple[int, int] = (35, 60)  # milli meter
    # light settings
    light_energy: Tuple[int, int] = (500, 1000)
    distance_light_camera: Tuple[int, int] = (1, 50)  # milli meter

    # Object position as coordinate origin
    object_position = np.array([0, 0, 0])
    output_dir.mkdir(parents=True, exist_ok=True)
    for i in range(n_images):


        random.seed(i)
        if objpath and Path(objpath).exists():
            objs = bproc.loader.load_obj(objpath)
            obj = objs[0]
        else:
            # Create a simple default object:
            obj = bproc.object.create_primitive("MONKEY")
            # position object right in the origin
        obj.set_location([0, 0, 0])
        obj.set_rotation_euler([0, 0, 0])

        add_texture(image_dir, obj)

        color = color2rgb(background_color)
        bproc.renderer.set_world_background(list(color))

        dist_obj_cam = random.uniform(min(distance_object_camera), max(distance_object_camera))
        dist_light_cam = random.uniform(min(distance_light_camera), max(distance_light_camera))
        #print(dist_obj_cam, dist_light_cam)
        # brighter
        brightness1 = random.uniform(min(light_energy), max(light_energy))
        #print(brightness1, brightness2)
        theta = random.uniform(0, max_theta)
        phi = random.uniform(0, max_phi)
        #print(theta, phi)

        camera_position = change_to_spherical(theta, phi, dist_obj_cam)

        rotation_euler = look_at(camera_position, object_position)
        #cam = create_camera(camera_position, rotation_euler)
        #print(f"Camera Position: {camera_position}, Rotation: {rotation_euler}")
        cam_pose = bproc.math.build_transformation_mat(camera_position, rotation_euler)

        bproc.camera.add_camera_pose(cam_pose)

        # get two simple vectors which perpendicular to v
        perp1, perp2 = create_perpendicular_vector(camera_position)

        circle_x, circle_y = random_point_on_unit_circle()

        # light position
        light_position = camera_position + circle_x * perp1 + circle_y * perp2
        choose_and_set_light(light_position, brightness1, p=light_percentage)

        data = bproc.renderer.render()
        for index, image in enumerate(data["colors"]):
            save_array_as_image(image, "colors", os.path.join(output_dir, f"image{index}.png"))









