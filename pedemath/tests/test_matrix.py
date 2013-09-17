
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
