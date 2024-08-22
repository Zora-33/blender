import blenderproc as bproc
import math
import random
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector, Matrix
from typing import Tuple, Union, List, Dict
from numpy.typing import NDArray

def read_obj(filepath: Union[str, Path]) -> mesh.Mesh:
    ''' read stl file and return mesh object
    '''
    #CAD files are often converted to STL files when preparing a design for 3D printing.
    bproc.init()
    stl_obj = bproc.loader.load_stl(filepath)
    return stl_obj

def add_texture (image_dir: Union[str, Path]):
    materials = bproc.material.collect_all()
    # Find the material of the ground object
    ground_material = bproc.filter.one_by_attr(materials, "name", "Material.001")
    # Set its displacement based on its base color texture
    ground_material.set_displacement_from_principled_shader_value("Base Color", multiply_factor=1.5)
    # Collect all jpg images in the specified directory
    images = list(Path(image_dir).absolute().rglob("material_manipulation_sample_texture*.jpg"))
    for mat in materials:
        # Load one random image
        image = bpy.data.images.load(filepath=str(random.choice(images)))
        # Set it as base color of the current material
        mat.set_principled_shader_value("Base Color", image)

def choose_and_set_light(position:Union[List[float], Tuple[float, float, float], NDArray[np.float64]], light_percentage:float, energy:int):
    if not (0 <= light_percentage <= 100):
        raise ValueError("Percentage must be between 0 and 100.")
    light = bproc.types.Light()
    if random.random() * 100 < percentage:
        # creat bar light
        light.set_type("AREA")
        light.set_size(2.0, 0.2)
    else:
        #create point light if greater the user-defined percentage
        light.set_type("POINT")
    light.set_energy(energy)
    light_object = light.get_object()
    light_object.set_location(position.tolist())

def parse_color(color_str:string) -> Tuple[float, float, float]:
    """
    Parses a user-defined color string and converts it to an RGB tuple that Blender can use.
    """
    # judgment the formate 'R,G,B' or '#RRGGBB'
    if re.match(r'^#([0-9A-Fa-f]{6})$', color_str):
        color_str = color_str.lstrip('#')
        r = int(color_str[0:2], 16) / 255.0  #hexadecimal
        g = int(color_str[2:4], 16) / 255.0
        b = int(color_str[4:6], 16) / 255.0
    elif re.match(r'^\d+,\d+,\d+$', color_str):
        r, g, b = map(int, color_str.split(','))
        r /= 255.0
        g /= 255.0
        b /= 255.0
    else:
        raise ValueError("Color must be in the format 'R,G,B' or '#RRGGBB'.")
    return (r, g, b)


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

    # USER INPUT
    #n_images: int = 10
    parser = argparse.ArgumentParser()
    # path
    parser.add_argument('image_dir', nargs='?', default="images",
                        help="Path to a folder with .jpg textures to be used in the sampling process")
    parser.add_argument('filepath', type=str, help='The path to the STL file to load.')
    parser.add_argument('output_dir', type=str, help='Directory to save rendered images.')
    #parameters
    parser.add_argument('Max_theta', help= 'Maximum angle of user input for theta ',
                        type= float)
    parser.add_argument('Max_phi', help= 'Maximum angle of user input for phi ',
                        type= float)
    parser.add_argument('n_images', help='How many images to generate ',
                        type= int)
    parser.add_argument('light_percentage', help='The user-defined percentage for the bar light',
                        type= float)
    parser.add_argument("--background-color", type=str, default="#FFFFFF",
                        help="Background color in 'R,G,B' or '#RRGGBB' format (default is white).")
    args = parser.parse_args()


    distance_object_camera: Tuple[int, int] = (10, 15)  # milli meter
    # light settings
    light_energy: Tuple[int, int] = (300, 600)
    distance_light_camera: Tuple[int, int] = (1, 50)  # milli meter

    # Object position as coordinate origin
    object_position = np.array([0, 0, 0])

    # load the stl file
    obj = read_obj(args.filepath)
    obj.set_location(object_position)
    obj.set_rotation_euler([0, 0, 0])

    # add texture to obj
    add_texture(args.image_dir)

    #set the background color
    color = parse_color(args.background_color)
    bproc.renderer.set_world_background(color)

    # for reproducibility set seed of pseudo-random number generator
    random.seed(42)

    # TODO: create loop
    # TODO: modularize script, i.e. put into self-contained functions
    for i in range(args.n_images):
        # randomness
        dist_obj_cam = random.uniform(min(distance_object_camera), max(distance_object_camera))
        dist_light_cam = random.uniform(min(distance_light_camera), max(distance_light_camera))
        brightness = random.uniform(min(light_energy), max(light_energy))

        theta = random.uniform(0, args.Max_theta)
        phi = random.uniform(0, args.Max_phi)

        camera_position = change_to_spherical(theta, phi, dist_obj_cam)
        rotation_euler = look_at(camera_position, object_position)
        cam_pose = bproc.math.build_transformation_mat(camera_position, rotation_euler)

        bproc.camera.add_camera_pose(cam_pose)

        # Light position will be in solar coordinate from a random distribution

        # Create a point light next to it

        cam_pose = bproc.math.build_transformation_mat(
            [0, -5, 0],[np.pi / 2, 0, 0]
        )
        bproc.camera.add_camera_pose(cam_pose)

        # get two simple vectors which perpendicular to v
        perp1, perp2 = create_perpendicular_vector(camera_position)

        circle_x, circle_y = random_point_on_unit_circle()

        # light position
        light_position = camera_position + circle_x * perp1 + circle_y * perp2
        choose_and_set_light(light_position,light_percentage, brightness)

        bproc.renderer.set_output_format(file_format="PNG")
        # image ratio 4:3
        bpy.context.scene.render.resolution_x = 640
        bpy.context.scene.render.resolution_y = 544
        bpy.context.scene.cycles.samples = 100

        output_dir = args.output_dir
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        bproc.renderer.set_output_path(os.path.join(args.output_dir, "render_{}.png".format(i)))
        bproc.renderer.render()