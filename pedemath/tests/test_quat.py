
import math
import unittest

from pedemath.matrix import Matrix44
from pedemath.quat import Quat
from pedemath.vec3 import Vec3


def AssertQuatAlmostEqual(quat1, quat2, tc):
    for comp in ("xyzw"):
        tc.assertAlmostEqual(getattr(quat1, comp), getattr(quat2, comp))


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

        # 90 deg around z moves x from positive to negative
        self.assertAlmostEqual(-1.0, rotated_vec.x)
        self.assertAlmostEqual(1.0, rotated_vec.y)
        self.assertAlmostEqual(1.0, rotated_vec.z)

    def test_rotate_vec_y(self):
        """Ensure resulting rotated vector is correct."""

        quat = Quat.from_axis_angle(Vec3(0, 1, 0), 90.)
        vec = Vec3(1, 1, 1)

        rotated_vec = quat.rotate_vec(vec)

        # 90 deg around y moves z from positive to negative
        self.assertAlmostEqual(1.0, rotated_vec.x)
        self.assertAlmostEqual(1.0, rotated_vec.y)
        self.assertAlmostEqual(-1.0, rotated_vec.z)

    def test_rotate_vec_x(self):
        """Ensure resulting rotated vector is correct."""

        quat = Quat.from_axis_angle(Vec3(1, 0, 0), 90.)
        vec = Vec3(1, 1, 1)

        rotated_vec = quat.rotate_vec(vec)

        # 90 deg around x moves y from positive to negative
        self.assertAlmostEqual(1.0, rotated_vec.x)
        self.assertAlmostEqual(-1.0, rotated_vec.y)
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


class FromMatrix44TestCase(unittest.TestCase):
    """Test Quat.from_matrix44()."""

    def test_x_rot(self):
        """Test that Quat.from_mat() works correctly for an x rotation."""

        # Create a Matrix representing 90 deg x rot.
        mat = Matrix44.from_rot_x(90)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure the quat matches a 90 degree x rotation.
        expected = Quat.from_axis_angle(Vec3(1, 0, 0), 90)
        AssertQuatAlmostEqual(quat, expected, self)

    def test_y_rot(self):
        """Test that Quat.from_mat() works correctly for an y rotation."""

        # Create a Matrix representing 90 deg y rot.
        mat = Matrix44.from_rot_y(90)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure the quat matches a 90 degree x rotation.
        expected = Quat.from_axis_angle(Vec3(0, 1, 0), 90)
        AssertQuatAlmostEqual(quat, expected, self)

    def test_z_rot(self):
        """Test that Quat.from_mat() works correctly for an z rotation."""

        # Create a Matrix representing 90 deg z rot.
        mat = Matrix44.from_rot_z(90)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure the quat matches a 90 degree x rotation.
        expected = Quat.from_axis_angle(Vec3(0, 0, 1), 90)
        AssertQuatAlmostEqual(quat, expected, self)

    def test_neg_x_rot(self):
        """Test that Quat.from_mat() works correctly for a negative x
        rotation.
        """

        # Create a Matrix representing -90 deg x rot.
        mat = Matrix44.from_rot_x(-90)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure the quat matches a -90 degree x rotation.
        expected = Quat.from_axis_angle(Vec3(1, 0, 0), -90)
        AssertQuatAlmostEqual(quat, expected, self)

    def test_small_x_rot(self):
        """Test that Quat.from_mat() works correctly for a negative x
        rotation.
        """

        # Create a Matrix representing 90 deg x rot.
        mat = Matrix44.from_rot_x(0.001)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure the quat matches the small degree x rotation.
        expected = Quat.from_axis_angle(Vec3(1, 0, 0), 0.001)
        self.assertAlmostEqual(quat.x, expected.x)
        self.assertAlmostEqual(quat.y, expected.y)
        self.assertAlmostEqual(quat.z, expected.z)
        self.assertAlmostEqual(quat.w, expected.w)

    def test_x_y_and_z_rot(self):
        """Test that Quat.from_mat() works correctly when there's a rotation
        on all axes.
        """

        axis = Vec3(4, 5, 6)
        # Create a Matrix representing a rotation.
        mat = Matrix44.from_axis_angle_deg(axis, 45.0)
        # Use from_matrix44()
        quat = Quat.from_matrix44(mat)

        # Ensure it matches the expected quaternion.
        expected_quat = Quat.from_axis_angle(axis, 45.0)
        self.assertAlmostEqual(quat.x, expected_quat.x)
        self.assertAlmostEqual(quat.y, expected_quat.y)
        self.assertAlmostEqual(quat.z, expected_quat.z)
        self.assertAlmostEqual(quat.w, expected_quat.w)


class TestConjugate(unittest.TestCase):
    """Test conjugate_quat() and Quat.conjugate()."""

    def test_conjugate(self):
        from pedemath.quat import conjugate_quat
        quat = Quat(1, 2, 3, 4)
        expected_quat = Quat(-1, -2, -3, 4)
        self.assertEqual(expected_quat, conjugate_quat(quat))

    def test_quat_conjugate(self):
        quat = Quat(1, 2, 3, 4)
        quat.conjugate()
        expected_quat = Quat(-1, -2, -3, 4)
        self.assertEqual(expected_quat, quat)


class TestEquality(unittest.TestCase):
    """Test Quat.__eq__."""

    def test_equality_with_quat(self):
        """Ensure that a basic equality check against two similar Quats returns
        True.
        """
        quat = Quat(1, 2, 3, 4)
        self.assertEqual(quat, Quat(1, 2, 3, 4))

    def test_equality_check_against_other_object_doesnt_raise_exception(self):
        """Ensure that when comparing with a different type, False is returned
        and an exception is not raised.
        """
        test_object = Vec3(1, 2, 3)
        self.assertFalse(test_object == Quat(1, 2, 3, 4))
        self.assertFalse(Quat(1, 2, 3, 4) == test_object)
        self.assertTrue(test_object != Quat(1, 2, 3, 4))
        self.assertTrue(Quat(1, 2, 3, 4) != test_object)

    def test_equality_check_against_basic_types_doesnt_raise_exception(self):
        test_int = 5
        test_str = "abc"
        self.assertFalse(test_int == Quat(1, 2, 3, 4))
        self.assertTrue(test_int != Quat(1, 2, 3, 4))
        self.assertFalse(test_str == Quat(1, 2, 3, 4))
        self.assertTrue(test_str != Quat(1, 2, 3, 4))


# class TestGetYRot(unittest.TestCase):
#     """Test get_y_rot_deg() and get_y_rot_rads()."""
#
#     def test_get_y_rot_no_rot(self):
#         quat = Quat()
#         self.assertEqual(0.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_neg_90_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, -89)
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(-89.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_from_x_and_z_rots(self):
#         x_axis = Vec3(1, 0, 0)
#         z_axis = Vec3(0, 0, 1)
#         quat = Quat.from_axis_angle(x_axis, 45)
#         quat_z = Quat.from_axis_angle(z_axis, 45)
#         logging.info(quat)
#         logging.info(quat_z)
#
#         # IMPLEMENTATION OF *= MIGHT BE WRONG
#         quat *= quat_z
#
#         logging.info("A: {}".format(quat * quat_z))
#         logging.info("A2: {}".format(
#             (quat * quat_z).get_y_tmp() * 180 / math.pi))
#         logging.info(quat)
#
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(-30.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_30_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 30)
#         self.assertAlmostEqual(30.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_90_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 90)
#         # print("If rot 1, 0, 1 by 90: {}".format(quat.rotate_vec(
#         #    Vec3(1, 0, 1))))
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(90.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_120_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 120)
#         logging.info("QUAT: {}".format(quat))
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(120.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_180_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 180)
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(180.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_210_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 210)
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(-150.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_270_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 270)
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(-90.0, quat.get_y_rot_deg())
#
#     def test_get_y_rot_330_rot(self):
#         y_axis = Vec3(0, 1, 0)
#         quat = Quat.from_axis_angle(y_axis, 330)
#         logging.info(quat.get_y_tmp() * 180 / math.pi)
#         self.assertAlmostEqual(-30.0, quat.get_y_rot_deg())
