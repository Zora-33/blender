import unittest
import numpy as np

from CosyTrafo import (
    # ----- Basic Mathematical Operations for Polar Coordinates
    add_polar_coordinates,
    add_spherical_coordinates,
    # ----- Coordinate Transform
    cylindrical_to_spherical,
    spherical_to_cylindrical,
    spherical_to_cartesian,
    cartesian_to_spherical,
    polar_to_cartesian
)


class CoordinateTransformationTest(unittest.TestCase):
    # POLAR ANGLE +-180!
    p1_o_x = (2, 2, 2)  # (x, y, z)
    p1_o_s = (3.46410161513775458705, 54.73561031724534568462, 45)  # (radius, polar angle, azimuth angle)

    p2_o_x = (1, 2, 3)
    p2_o_s = (3.74165738677394138558, 36.69922520048988301023, 63.43494882292201064843)
    # p1 + p2
    p1_p2_x = (3, 4, 5)
    p1_p2_s = (7.07106781186547524401, 45, 53.13010235415597870314)

    p3_o_x = (30.6417777247591214081, 25.71150438746157305291, 0)
    p3_o_s = (40, 90, 40)

    decimal_accuracy = 10

    def test_spherical2cartesian_p1(self):
        p1_o_x_test = spherical_to_cartesian(*self.p1_o_s, degree=True)
        np.testing.assert_almost_equal(p1_o_x_test, self.p1_o_x, decimal=self.decimal_accuracy)

    def test_cartesian2spherical_p1(self):
        p1_o_s_test = cartesian_to_spherical(*self.p1_o_x, degree=True)
        np.testing.assert_almost_equal(p1_o_s_test, self.p1_o_s, decimal=self.decimal_accuracy)

    def test_cartesian2spherical_p2(self):
        p2_o_s_test = cartesian_to_spherical(*self.p2_o_x, degree=True)
        np.testing.assert_almost_equal(p2_o_s_test, self.p2_o_s, decimal=self.decimal_accuracy)

    def test_cartesian2spherical_p1_p2(self):
        p1_p2_o_s_test = cartesian_to_spherical(*self.p1_p2_x, degree=True)
        np.testing.assert_almost_equal(p1_p2_o_s_test, self.p1_p2_s, decimal=self.decimal_accuracy)

    def test_spherical2cartesian_cartesian2spherical_p1(self):
        p1_o_s_test = cartesian_to_spherical(*spherical_to_cartesian(*self.p1_o_s, degree=True), degree=True)
        np.testing.assert_almost_equal(p1_o_s_test, self.p1_o_s, decimal=self.decimal_accuracy)

    def test_add_spherical_coordinates_p1_p2(self):
        p1_p2_s_test = add_spherical_coordinates(self.p1_o_s, self.p2_o_s, degree=True)
        np.testing.assert_almost_equal(p1_p2_s_test, self.p1_p2_s, decimal=self.decimal_accuracy)

    def test_add_spherical_coordinates_in_cartesian_p1_p2(self):
        p1_p2_x_test1 = spherical_to_cartesian(
            *add_spherical_coordinates(self.p1_o_s, self.p2_o_s, degree=True),
            degree=True)

        p1_p2_x_test2 = tuple([np.sum(el) for el in zip(spherical_to_cartesian(*self.p1_o_s, degree=True),
                                                        spherical_to_cartesian(*self.p2_o_s, degree=True))])
        print(f"DEBUGGING: p1_p2_x_test1={p1_p2_x_test1} p1_p2_x_test2={p1_p2_x_test2} self.p1_p2_x={self.p1_p2_x}")
        # check "relative" correctness
        np.testing.assert_almost_equal(p1_p2_x_test1, p1_p2_x_test2, decimal=self.decimal_accuracy)
        # check absolute correct
        np.testing.assert_almost_equal(p1_p2_x_test1, self.p1_p2_x, decimal=self.decimal_accuracy)
        np.testing.assert_almost_equal(p1_p2_x_test2, self.p1_p2_x, decimal=self.decimal_accuracy)

    def test_cartesian2spherical_p3(self):
        p3_o_s_test = cartesian_to_spherical(*self.p3_o_x, degree=True)
        np.testing.assert_almost_equal(p3_o_s_test, self.p3_o_s, decimal=self.decimal_accuracy)

    def test_spherical2cartesian_p3(self):
        p3_o_x_test = spherical_to_cartesian(*self.p3_o_s, degree=True)
        np.testing.assert_almost_equal(p3_o_x_test, self.p3_o_x, decimal=self.decimal_accuracy)


if __name__ == '__main__':
    unittest.main()



