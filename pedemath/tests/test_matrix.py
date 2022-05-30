
import math
import unittest

from pedemath.vec3 import Vec3
from pedemath.matrix import Matrix44


class TestMatrix44MakeIdentity(unittest.TestCase):
    """Test Matrix44.make_identity()."""

    def test_make_identity(self):
        """Ensure identity matrix is correct."""

        mat = Matrix44()
        mat.make_identity()
        for i in range(4):
            for j in range(4):
                if j == i:
                    self.assertEqual(1, mat.data[j][i])
                else:
                    self.assertEqual(0, mat.data[j][i])

class TestMatrix44GetTrans(unittest.TestCase):
    """Test Matrix44.get_trans()."""

    def test_vec3_returned(self):
        """Ensure the position arguments are returned as a Vec3."""
        matrix = Matrix44()
        matrix.data[3][0] = 1
        matrix.data[3][1] = 2
        matrix.data[3][2] = 3

        self.assertEqual(Vec3(1, 2, 3), matrix.get_trans())

    def test_with_out_vec_arg(self):
        """Ensure the position arguments are inserted into the Vec3 out_vec
        arg and the out_vec is also returned.
        """
        matrix = Matrix44()
        out_vec = Vec3(0, 0, 0)
        matrix.data[3][0] = -1
        matrix.data[3][1] = -2
        matrix.data[3][2] = -3

        result = matrix.get_trans(out_vec)
        self.assertEqual(Vec3(-1, -2, -3), result)
        self.assertIs(out_vec, result)


class TestMatrix44MakeRot(unittest.TestCase):
    """Test Matrix44.from_rot_x(), from_rot_y() and from_rot_z()."""

    def test_from_rot_x(self):
        """Ensure x rotation matrix is created correctly."""

        mat = Matrix44().from_rot_x(30)

        # Ensure column-major result
        self.assertAlmostEqual(mat.data[1][1], math.sqrt(3) / 2.0)
        self.assertEqual(mat.data[2][1], -1.0 / 2.0)
        self.assertEqual(mat.data[1][2], 1.0 / 2.0)
        self.assertAlmostEqual(mat.data[2][2], math.sqrt(3) / 2.0)

    def test_from_rot_y(self):
        """Ensure y rotation matrix is created correctly."""

        mat = Matrix44().from_rot_y(30)

        # Ensure column-major result
        self.assertAlmostEqual(mat.data[0][0], math.sqrt(3) / 2.0)
        self.assertEqual(mat.data[2][0], 1.0 / 2.0)
        self.assertEqual(mat.data[0][2], -1.0 / 2.0)
        self.assertAlmostEqual(mat.data[2][2], math.sqrt(3) / 2.0)

    def test_from_rot_z(self):
        """Ensure z rotation matrix is created correctly."""

        mat = Matrix44().from_rot_z(30)

        # Ensure column-major result
        self.assertAlmostEqual(mat.data[0][0], math.sqrt(3) / 2.0)
        self.assertEqual(mat.data[1][0], -1.0 / 2.0)
        self.assertEqual(mat.data[0][1], 1.0 / 2.0)
        self.assertAlmostEqual(mat.data[1][1], math.sqrt(3) / 2.0)


class Matrix44OpsTestCase(unittest.TestCase):
    """Test add and subtract matrix operations."""

    def test_add(self):
        m = Matrix44()

        m2 = Matrix44()
        for i in range(4):
            for j in range(4):
                m.data[i][j] = i * 1000 + j * 100
                m2.data[i][j] = i * 10 + j

        result = (m + m2)

        for i in range(4):
            for j in range(4):
                self.assertEqual(result.data[i][j],
                                 i * 1000 + j * 100 + i * 10 + j)

    def test_subtract(self):
        m = Matrix44()

        m2 = Matrix44()
        for i in range(4):
            for j in range(4):
                m.data[i][j] = i * 1000 + j * 100
                m2.data[i][j] = i * 10 + j

        result = (m - m2)

        for i in range(4):
            for j in range(4):
                self.assertEqual(result.data[i][j],
                                 i * 1000 + j * 100 - (i * 10 + j))


class Matrix44MultTestCase(unittest.TestCase):
    """Test matrix multiplication."""

    def test_multiply(self):
        """Test simple matrix multiplication."""

        from numpy import array
        column_major_order = "F"

        m1 = Matrix44()

        m2 = Matrix44()
        for i in range(4):
            m1.data[0][i] = (i+1)
            m2.data[i][0] = (i+1) * 10

        # |1 0 0 0|     |10 20 30 40|
        # |2 1 0 0|  *  |0 1 0 0|
        # |3 0 1 0|     |0 0 1 0|
        # |4 0 0 1|     |0 0 0 1|

        result = (m1 * m2)

        expected_array = array([
            [10, 20, 30, 40],  # Note: columns look like rows here
            [20, 41, 60, 80],
            [30, 60, 91, 120],
            [40, 80, 120, 161]], dtype="float32",
            order=column_major_order)

        for i in range(4):
            for j in range(4):
                self.assertEqual(result.data[i][j],
                                 expected_array[i][j])

    def test_r_multiply(self):
        """Test __rmul__ matrix multiplication.

        Example: matrix1 *= matrix2
        """

        from numpy import array
        column_major_order = "F"

        m1 = Matrix44()

        m2 = Matrix44()
        for i in range(4):
            m1.data[0][i] = (i+1)
            m2.data[i][0] = (i+1) * 10

        # |1 0 0 0|     |10 20 30 40|
        # |2 1 0 0|  *  |0 1 0 0|
        # |3 0 1 0|     |0 0 1 0|
        # |4 0 0 1|     |0 0 0 1|

        m1 *= m2

        expected_array = array([
            [10, 20, 30, 40],  # Note: columns look like rows here
            [20, 41, 60, 80],
            [30, 60, 91, 120],
            [40, 80, 120, 161]], dtype="float32",
            order=column_major_order)

        for i in range(4):
            for j in range(4):
                self.assertEqual(m1.data[i][j],
                                 expected_array[i][j])

    def test_multiply_b(self):
        """Test matrix multiplication with all non-zero values."""

        from numpy import array
        column_major_order = "F"

        m1 = Matrix44()

        m2 = Matrix44()
        for col in range(4):
            for row in range(4):
                m1.data[col][row] = col * 4 + row + 1
                m2.data[col][row] = 1

        # |1 5  9 13|     |1 1 1 1|   |28 28 28 28|
        # |2 6 10 14|  *  |1 1 1 1| = |32 32 32 32|
        # |3 7 11 15|     |1 1 1 1|   |36 36 36 36|
        # |4 8 12 16|     |1 1 1 1|   |40 40 40 40|

        result = (m1 * m2)

        expected_array = array([
            [28, 32, 36, 40],  # Note: columns look like rows here
            [28, 32, 36, 40],
            [28, 32, 36, 40],
            [28, 32, 36, 40]], dtype="float32",
            order=column_major_order)

        for i in range(4):
            for j in range(4):
                self.assertEqual(result.data[i][j],
                                 expected_array[i][j])

    def test_multiply_c(self):
        """Test matrix multiplication with all non-zero values."""

        from numpy import array
        column_major_order = "F"

        m1 = Matrix44()

        m2 = Matrix44()
        for col in range(4):
            for row in range(4):
                m1.data[col][row] = 1
                m2.data[col][row] = col * 4 + row + 1

        # |1 1 1 1|   |1 5  9 13|
        # |1 1 1 1| + |2 6 10 14|
        # |1 1 1 1|   |3 7 11 15|
        # |1 1 1 1|   |4 8 12 16|

        result = (m1 * m2)

        expected_array = array([
            [10, 10, 10, 10],  # Note: columns look like rows here
            [26, 26, 26, 26],
            [42, 42, 42, 42],
            [58, 58, 58, 58]], dtype="float32",
            order=column_major_order)

        for i in range(4):
            for j in range(4):
                self.assertEqual(result.data[i][j],
                                 expected_array[i][j])

    def test_multiply_d(self):
        """
        Test matrix multiplication of two matrices containing mostly all unique
        values.
        """

        from numpy import array
        column_major_order = "F"

        m1 = Matrix44()

        m2 = Matrix44()
        for col in range(4):
            for row in range(4):
                m1.data[col][row] = col * 4 + row + 1
                m2.data[col][row] = (col * 4 + row + 1) * 10

        # |1 5  9 13|     |10 50  90 130|
        # |2 6 10 14|  *  |20 60 100 140|
        # |3 7 11 15|     |30 70 110 150|
        # |4 8 12 16|     |40 80 120 160|

        # a e i m
        # b f j n
        # c g k o
        # d h l p

        # Examples:
        # c = 3 * 10 + 7 * 20 + 11 * 30 + 15 * 40 = 1100
        # j = 2 * 90 + 6 * 100 + 10 * 110 + 14 * 120 = 3560
        # o = 3 * 130 + 7 * 140 + 11 * 150 + 15 * 160 = 5420
        # l = 4 * 90 + 8 * 100 + 12 * 110 + 16 * 120 = 4400
        # m = 1 * 130 + 5 * 140 + 9 * 150 + 13 * 160 = 4260
        # n = 2 * 130 + 6 * 140 + 10 * 150 + 14 * 160 = 4840
        # p = 4 * 130 + 8 * 140 + 12 * 150 + 16 * 160 = 6000
        result = (m1 * m2)

        expected_array = array([
            [900, 1000, 1100, 1200],  # Note: columns look like rows here
            [2020, 2280, 2540, 2800],
            [3140, 3560, 3980, 4400],
            [4260, 4840, 5420, 6000]], dtype="float32",
            order=column_major_order)

        for col in range(4):
            for row in range(4):
                self.assertEqual(result.data[col][row],
                                 expected_array[col][row])


class InvertAffineMat44TestCase(unittest.TestCase):
    """Test invert_affine_mat44()'s ability to invert affine matrices."""

    def test_invert_mat4(self):
        """Ensure that a transform matrix * its
        invert is an identity matrix.
        """

        from pedemath.quat import Quat
        from pedemath.matrix import invert_affine_mat44

        mat = Quat.from_axis_angle(Vec3(-1, 2, -3), -40).as_matrix44()
        trans_mat = Matrix44.from_trans((-7, -8, -9))
        mat *= trans_mat

        inverted = invert_affine_mat44(mat)
        ident = Matrix44()

        self.assertTrue(ident.almost_equal(mat * inverted, places=5))
        self.assertTrue(ident.almost_equal(inverted * mat))

    def test_invert_transform_transform_pt(self):
        """Ensure that invert_transform can produce
        a matrix that reverts a transformed point to
        its original value.
        """

        from pedemath.quat import Quat
        from pedemath.matrix import invert_affine_mat44

        mat1 = Quat.from_axis_angle(Vec3(1, 2, 3), 40).as_matrix44()
        trans_mat1 = Matrix44.from_trans((-7, -8, 9))
        mat1 *= trans_mat1

        mat2 = Quat.from_axis_angle(Vec3(-5, 2, -4), 40).as_matrix44()
        trans_mat2 = Matrix44.from_trans((-2, -5, 3))
        mat2 *= trans_mat2

        combined_mat = mat1 * mat2

        combined_mat_inverse = invert_affine_mat44(combined_mat)

        pt = Vec3(3, -4, 5)

        # Transform point
        transformed_pt = combined_mat * pt
        # Transform with inverse of matrix.
        reverted_pt = combined_mat_inverse * transformed_pt

        self.assertTrue(pt.almost_equal(reverted_pt, 5))

        # Also inverse mat1 and mat2 individually.
        mat1_inverse = invert_affine_mat44(mat1)
        mat2_inverse = invert_affine_mat44(mat2)

        self.assertTrue(
            combined_mat_inverse.almost_equal(
                mat2_inverse * mat1_inverse, places=5))


class Matrix44FromAxisAngleTestCase(unittest.TestCase):
    """Test Matrix44.from_axis_angle_deg()."""

    def test_x_rot(self):
        """Test Matrix44.from_axis_angle_deg() with an x rotation."""

        mat = Matrix44.from_axis_angle_deg(Vec3(1, 0, 0), 90)

        # Column 0
        self.assertAlmostEqual(mat.data[0][0], 1)
        self.assertAlmostEqual(mat.data[0][1], 0)
        self.assertAlmostEqual(mat.data[0][2], 0)
        self.assertAlmostEqual(mat.data[0][3], 0)
        # Column 1
        self.assertAlmostEqual(mat.data[1][0], 0)
        self.assertAlmostEqual(mat.data[1][1], 0)
        self.assertAlmostEqual(mat.data[1][2], 1)
        self.assertAlmostEqual(mat.data[1][3], 0)
        # Column 2
        self.assertAlmostEqual(mat.data[2][0], 0)
        self.assertAlmostEqual(mat.data[2][1], -1)
        self.assertAlmostEqual(mat.data[2][2], 0)
        self.assertAlmostEqual(mat.data[2][3], 0)
        # Column 3
        self.assertAlmostEqual(mat.data[3][0], 0)
        self.assertAlmostEqual(mat.data[3][1], 0)
        self.assertAlmostEqual(mat.data[3][2], 0)
        self.assertAlmostEqual(mat.data[3][3], 1)

    def test_y_rot(self):
        """Test Matrix44.from_axis_angle_deg() with a y rotation."""

        mat = Matrix44.from_axis_angle_deg(Vec3(0, 1, 0), 90)

        # Column 0
        self.assertAlmostEqual(mat.data[0][0], 0)
        self.assertAlmostEqual(mat.data[0][1], 0)
        self.assertAlmostEqual(mat.data[0][2], -1)
        self.assertAlmostEqual(mat.data[0][3], 0)
        # Column 1
        self.assertAlmostEqual(mat.data[1][0], 0)
        self.assertAlmostEqual(mat.data[1][1], 1)
        self.assertAlmostEqual(mat.data[1][2], 0)
        self.assertAlmostEqual(mat.data[1][3], 0)
        # Column 2
        self.assertAlmostEqual(mat.data[2][0], 1)
        self.assertAlmostEqual(mat.data[2][1], 0)
        self.assertAlmostEqual(mat.data[2][2], 0)
        self.assertAlmostEqual(mat.data[2][3], 0)
        # Column 3
        self.assertAlmostEqual(mat.data[3][0], 0)
        self.assertAlmostEqual(mat.data[3][1], 0)
        self.assertAlmostEqual(mat.data[3][2], 0)
        self.assertAlmostEqual(mat.data[3][3], 1)

    def test_z_rot(self):
        """Test Matrix44.from_axis_angle_deg() with a z rotation."""

        mat = Matrix44.from_axis_angle_deg(Vec3(0, 0, 1), 90)

        # Column 0
        self.assertAlmostEqual(mat.data[0][0], 0)
        self.assertAlmostEqual(mat.data[0][1], 1)
        self.assertAlmostEqual(mat.data[0][2], 0)
        self.assertAlmostEqual(mat.data[0][3], 0)
        # Column 1
        self.assertAlmostEqual(mat.data[1][0], -1)
        self.assertAlmostEqual(mat.data[1][1], 0)
        self.assertAlmostEqual(mat.data[1][2], 0)
        self.assertAlmostEqual(mat.data[1][3], 0)
        # Column 2
        self.assertAlmostEqual(mat.data[2][0], 0)
        self.assertAlmostEqual(mat.data[2][1], 0)
        self.assertAlmostEqual(mat.data[2][2], 1)
        self.assertAlmostEqual(mat.data[2][3], 0)
        # Column 3
        self.assertAlmostEqual(mat.data[3][0], 0)
        self.assertAlmostEqual(mat.data[3][1], 0)
        self.assertAlmostEqual(mat.data[3][2], 0)
        self.assertAlmostEqual(mat.data[3][3], 1)
