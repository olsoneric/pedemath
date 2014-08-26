
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
