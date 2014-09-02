
import math
import unittest

from pedemath.matrix import Matrix44
from pedemath.quat import Quat
from pedemath.vec3 import Vec3


#class TestQuatIntegration(unittest.TestCase):
#
#    def test_rot_90_x_90_y(self):
#
#        x_quat = Quat.from_axis_angle(Vec3(1, 0, 0), 90)
#        y_quat = Quat.from_axis_angle(Vec3(0, 1, 0), 90)
#
#        matrix = (y_quat * x_quat).get_rot_matrix()
#
#        pos = Vec3(0, 1, 0)
#        new_pos = matrix * pos
#        expected_new_pos = Vec3(1, 0, 0)
#        for i in range(3):
#            self.assertAlmostEqual(new_pos[i], expected_new_pos[i])
#

class TestFromAxisAngle(unittest.TestCase):
    """Test Quat.from_axis_angle."""

    def test_180_x(self):

        x_quat = Quat.from_axis_angle(Vec3(1, 0, 0), 180)
        expected = Quat(1, 0, 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], x_quat[i])

    def test_180_y(self):

        y_quat = Quat.from_axis_angle(Vec3(0, 1, 0), 180)
        expected = Quat(0, 1, 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], y_quat[i])

    def test_180_z(self):

        z_quat = Quat.from_axis_angle(Vec3(0, 0, 1), 180)
        expected = Quat(0, 0, 1, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], z_quat[i])

    def test_90_x(self):

        x_quat = Quat.from_axis_angle(Vec3(1, 0, 0), 90)
        expected = Quat(math.sqrt(0.5), 0, 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], x_quat[i])

    def test_90_y(self):

        y_quat = Quat.from_axis_angle(Vec3(0, 1, 0), 90)
        expected = Quat(0, math.sqrt(0.5), 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], y_quat[i])

    def test_90_z(self):

        z_quat = Quat.from_axis_angle(Vec3(0, 0, 1), 90)
        expected = Quat(0, 0, math.sqrt(0.5), 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], z_quat[i])

    def test_neg_90_x(self):

        x_quat = Quat.from_axis_angle(Vec3(1, 0, 0), -90)
        expected = Quat(-math.sqrt(0.5), 0, 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], x_quat[i])

    def test_neg_90_y(self):

        y_quat = Quat.from_axis_angle(Vec3(0, 1, 0), -90)
        expected = Quat(0, -math.sqrt(0.5), 0, 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], y_quat[i])

    def test_neg_90_z(self):

        z_quat = Quat.from_axis_angle(Vec3(0, 0, 1), -90)
        expected = Quat(0, 0, -math.sqrt(0.5), 0)

        for i in range(3):
            self.assertAlmostEqual(expected[i], z_quat[i])


class TestAsMatrix44TestCase(unittest.TestCase):
    """Test Quat.as_matrix44()."""

    def test_as_matrix44(self):
        quat = Quat(0, 0, 0, 1)
        mat = quat.as_matrix44()

        self.assertTrue(mat == Matrix44())

    def test_get_matrix_45_x(self):
        # 45 deg x rotation
        quat = Quat.from_axis_angle(Vec3(1, 0, 0), 45.)
        mat_from_quat = quat.as_matrix44()
        mat = Matrix44.from_rot_x(45.)

        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(mat.data[j][i],
                                       mat_from_quat.data[j][i])

    def test_get_matrix_45_y(self):
        # 45 deg y rotation
        quat = Quat.from_axis_angle(Vec3(0, 1, 0), 45.)
        mat_from_quat = quat.as_matrix44()
        mat = Matrix44.from_rot_y(45.)

        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(mat.data[j][i],
                                       mat_from_quat.data[j][i])

    def test_get_matrix_45_z(self):
        # 45 deg z rotation
        quat = Quat.from_axis_angle(Vec3(0, 0, 1), 45.)
        mat_from_quat = quat.as_matrix44()
        mat = Matrix44.from_rot_z(45.)

        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(mat.data[j][i],
                                       mat_from_quat.data[j][i])

class RotateVecTestCase(unittest.TestCase):
    """Test Quat.rotate_vec."""

    def test_rotate_vec_z(self):
        """Ensure resulting vector is correct."""

        quat = Quat.from_axis_angle(Vec3(0, 0, 1), 90.)
        vec = Vec3(1, 1, 1)

        rotated_vec = quat.rotate_vec(vec)

        self.assertAlmostEqual(-1.0, rotated_vec.x)
        self.assertAlmostEqual(1.0, rotated_vec.y)
        self.assertAlmostEqual(1.0, rotated_vec.z)

    def test_rotate_vec(self):
        """Ensure resulting vector is correct."""

        quat = Quat.from_axis_angle(Vec3(-1, -1, -1), 180.)
        vec = Vec3(1, 0, 0)

        rotated_vec = quat.rotate_vec(vec)

        self.assertAlmostEqual(-1/3.0, rotated_vec.x)
        self.assertAlmostEqual(2/3.0, rotated_vec.y)
        self.assertAlmostEqual(2/3.0, rotated_vec.z)
    # TODO: more rotate_vec angles tested?


