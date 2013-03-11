
# Copyright 2012-2013 Eric Olson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

from mock import patch

from pedemath.vec2 import Vec2


class Vec2InitTestCase(unittest.TestCase):
    """Test Vec2's constructor."""

    def test_members_are_set(self):
        """Ensure the x and y members are set."""

        v = Vec2(5.0, 6.0)

        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)

    def test_members_are_set_when_args_are_ints(self):
        """Ensure the x and y members are set.
        Ensure the members have been made float types.
        """

        v = Vec2(5, 6)

        # Assert member values are what we expect.
        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)

        # Assert member values are floats.
        self.assertTrue(isinstance(v.x, float))
        self.assertTrue(isinstance(v.y, float))

    def test_members_are_set_when_args_are_strs(self):
        """Ensure the x and y members are set.
        Ensure the members have been made float types.

        This isn't necessary functionality, but this works with python,
        so ensure this doesn't change without knowing it might break some
        existing code.  Also, don't want to add overhead in the constructor to
        explicitly disable this.
        """

        v = Vec2("5", "6")

        # Assert member values are what we expect.
        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)

        # Assert member values are floats.
        self.assertTrue(isinstance(v.x, float))
        self.assertTrue(isinstance(v.y, float))

    def test_members_are_set_when_args_are_invalid(self):
        """Ensure when an arg is invalid that ValueError is raised."""

        self.assertRaises(ValueError, Vec2, "abc", 6)


class Vec2AddTestCase(unittest.TestCase):
    """Test Vec2's __add__() which is used in Vec2 + Vec2."""

    def test_add_with_vec_argument(self):
        """Ensure that adding another vector returns another Vec2 with the
        right values.
        """

        a = Vec2(2, 3)
        b = Vec2(1, 1)

        result = a + b

        expected_result = Vec2(3, 4)

        self.assertEqual(result, expected_result)

    def test_add_with_float_arg(self):
        """Ensure that adding a float returns another Vec2 with the float
        added to x and y.
        """

        a = Vec2(2, 3)
        b = 5.0

        result = a + b

        expected_result = Vec2(7, 8)

        self.assertEqual(result, expected_result)

    def test_add_with_int_arg(self):
        """Ensure that adding a int returns another Vec2 with the int
        added to x and y.
        """

        a = Vec2(2, 3)
        b = 5

        result = a + b

        expected_result = Vec2(7, 8)

        self.assertEqual(result, expected_result)


class AddV2TestCase(unittest.TestCase):
    """Test add_v2(Vec2, Vec2)."""

    def test_add_with_vec_argument(self):
        """Ensure that adding another vector returns another Vec2 with the
        right values.
        """

        from pedemath.vec2 import add_v2

        a = Vec2(2, 3)
        b = Vec2(1, 1)

        result = add_v2(a, b)

        expected_result = Vec2(3, 4)

        self.assertEqual(result, expected_result)

    def test_add_with_float_arg(self):
        """Ensure that adding a float returns another Vec2 with the float
        added to x and y.
        """

        from pedemath.vec2 import add_v2

        a = Vec2(2, 3)
        b = 5.0

        result = add_v2(a, b)

        expected_result = Vec2(7, 8)

        self.assertEqual(result, expected_result)

    def test_add_with_int_arg(self):
        """Ensure that adding a int returns another Vec2 with the int
        added to x and y.
        """

        from pedemath.vec2 import add_v2

        a = Vec2(2, 3)
        b = 5

        result = add_v2(a, b)

        expected_result = Vec2(7, 8)

        self.assertEqual(result, expected_result)


class Vec2NegEqNeTestCase(unittest.TestCase):
    """Test Vec2's __neg__, __eq__, and __ne__."""

    def test_vec2_neg(self):
        """Ensure -Vec2 returns a Vec2 with -x and -y."""

        a = Vec2(2, 3)
        b = Vec2(-2, -3)

        self.assertEqual(-a, b)

    def test_vec2_eq_is_true(self):
        """Ensure -Vec2 returns a Vec2 with -x and -y."""

        a = Vec2(2, 3)
        b = Vec2(2, 3)

        self.assertTrue(a == b)

    def test_vec2_eq_is_false(self):
        """Ensure -Vec2 returns a Vec2 with -x and -y."""

        a = Vec2(2, 3)
        b = Vec2(2, -3)

        self.assertFalse(a == b)

    def test_vec2_ne_is_true(self):
        """Ensure -Vec2 returns a Vec2 with -x and -y."""

        a = Vec2(2, 3)
        b = Vec2(2, -3)

        self.assertTrue(a != b)

    def test_vec2_ne_is_false(self):
        """Ensure -Vec2 returns a Vec2 with -x and -y."""

        a = Vec2(2, 3)
        b = Vec2(2, 3)

        self.assertFalse(a != b)


class Vec2NormalizeTestCase(unittest.TestCase):
    """Ensure Vec2.normalize works as expected."""

    def test_normalize(self):
        """Normalize the component's so the vector's length is one."""

        a = Vec2(3, 4)
        a.normalize()

        expected_vec = Vec2(0.6, 0.8)

        self.assertAlmostEqual(a.x, expected_vec.x)
        self.assertAlmostEqual(a.y, expected_vec.y)

    def test_normalize_zero_length_vector(self):
        """If a vector is of length zero, normalizing it should fail
        gracefully and just leave it as a zero length vector.
        """

        a = Vec2(0, 0)

        a.normalize()

        self.assertEqual(Vec2(0, 0), a)


class NormalizeV2TestCase(unittest.TestCase):
    """Ensure Vec2.normalize works as expected."""

    def test_normalize(self):
        """Normalize the components so the vector's length is one."""

        from pedemath.vec2 import normalize_v2

        a = Vec2(3, 4)
        result = normalize_v2(a)

        expected_vec = Vec2(0.6, 0.8)

        self.assertAlmostEqual(result.x, expected_vec.x)
        self.assertAlmostEqual(result.y, expected_vec.y)

    def test_normalize_zero_length_vector(self):
        """If the vector is of length zero, a divide by zero error is
        raised when trying to normalize it.
        """

        from pedemath.vec2 import normalize_v2

        a = Vec2(0, 0)

        result = normalize_v2(a)

        self.assertEqual(Vec2(0, 0), result)


class Vec2TruncateTestCase(unittest.TestCase):
    """Ensure Vec2.truncate limits the vector to the max_length."""

    def test_truncate_when_greater_than_max_length(self):
        """Ensure the vector is scaled to the max_length."""

        a = Vec2(6, 8)

        # Truncate the vector of length 10 to one of length 5.
        a.truncate(5)

        expected_vec = Vec2(3, 4)

        self.assertEqual(a, expected_vec)

    @patch('pedemath.vec2.Vec2.scale')
    def test_truncate_when_less_than_max_length(self, scale):
        """Ensure the vector is not scaled since it is less than max_length."""

        a = Vec2(3, 4)

        # Call truncate(max_length=10) on the vector of length 5.
        a.truncate(10)

        # Expect no change
        expected_vec = Vec2(3, 4)

        # Ensure no change was made
        self.assertEqual(a, expected_vec)

        # Make sure Vec2.scale() was not called.
        self.assertFalse(scale.called)


class Vec2ScaleTestCase(unittest.TestCase):
    """Ensure Vec2.scale modifies the Vec2 correctly."""

    def test_vec2_scale(self):
        """Ensure the Vec2's x and y are scaled by the factor."""

        a = Vec2(7, 8)

        a.scale(2)

        self.assertEqual(a, Vec2(14, 16))

    def test_vec2_scale_of_zero(self):
        """Ensure the Vec2's x and y are scaled by zero with no errors."""

        a = Vec2(7, 8)

        a.scale(0)

        self.assertEqual(a, Vec2(0, 0))


class ScaleV2TestCase(unittest.TestCase):
    """Ensure scale_v2 creates a scaled Vec2 correctly."""

    def test_vec2_scale(self):
        """Ensure a new Vec2 is returned with a scaled x and y."""

        from pedemath.vec2 import scale_v2

        a = Vec2(7, 8)

        result_vec = scale_v2(a, 2)

        self.assertEqual(result_vec, Vec2(14, 16))

        # Ensure a new vector was returned.
        self.assertNotEqual(id(result_vec), id(a))

    def test_vec2_scale_of_zero(self):
        """Ensure the new Vec2's x and y are scaled to zero with no errors."""

        from pedemath.vec2 import scale_v2

        a = Vec2(7, 8)

        result_vec = scale_v2(a, 0)

        self.assertEqual(result_vec, Vec2(0, 0))

        # Ensure a new vector was returned.
        self.assertNotEqual(id(result_vec), id(a))


class Vec2GetScaleTestCase(unittest.TestCase):
    """Ensure Vec2.get_scale returns a new Vec2 that is scaled correctly."""

    def test_vec2_scale(self):
        """Ensure the returned Vec2's x and y are scaled by the factor."""

        a = Vec2(7, 8)

        result_vec = a.get_scaled_v2(2)

        self.assertEqual(result_vec, Vec2(14, 16))

        # Ensure a new vector was returned.
        self.assertNotEqual(id(result_vec), id(a))

    def test_vec2_scale_of_zero(self):
        """Ensure the Vec2's x and y are scaled by zero with no errors."""

        a = Vec2(7, 8)

        result_vec = a.get_scaled_v2(0)

        self.assertEqual(result_vec, Vec2(0, 0))

        # Ensure a new vector was returned.
        self.assertNotEqual(id(result_vec), id(a))


class Vec2SquareTestCase(unittest.TestCase):
    """Ensure Vec2's x and y have been squared."""

    def test_vec2_square(self):
        """Ensure Vec2's x and y have been squared."""

        a = Vec2(3, 4)

        a.square()

        self.assertEqual(a, Vec2(9, 16))


class SquareV2TestCase(unittest.TestCase):
    """Ensure a new Vec2 is returned with x squared and y squared."""

    def test_vec2_square(self):
        """Ensure Vec2's x and y have been squared."""

        from pedemath.vec2 import square_v2

        a = Vec2(3, 4)

        result = square_v2(a)

        self.assertEqual(result, Vec2(9, 16))


class Vec2GetSquareV2TestCase(unittest.TestCase):
    """Ensure a new Vec2 is returned with x squared and y squared."""

    def test_vec2_square(self):
        """Ensure Vec2's x and y have been squared."""

        a = Vec2(3, 4)

        result = a.get_square()

        self.assertEqual(result, Vec2(9, 16))


class Vec2GetNormTestCase(unittest.TestCase):
    """Ensure Vec2.get_norm returns the vector norm."""

    def test_vec2_get_norm(self):
        """Ensure Vec2.get_norm() returns x * x + y * y"""

        a = Vec2(3, 4)

        result = a.get_norm()

        self.assertEqual(result, 25.0)


class Vec2GetPerpTestCase(unittest.TestCase):
    """Ensure Vec2.get_perp returns a perpendicular vector."""

    def test_vec2_get_perp(self):
        """Ensure Vec2.get_perp() returns x * x + y * y"""

        a = Vec2(3, 4)

        result = a.get_perp()

        self.assertEqual(result, Vec2(-4, 3))


class Vec2LengthTestCase(unittest.TestCase):
    """Ensure Vec2.length returns the vector length."""

    def test_vec2_length(self):
        """Ensure Vec2.length() returns x * x + y * y"""

        a = Vec2(3, 4)

        result = a.length()

        self.assertEqual(result, 5.0)


class Vec2GetItemTestCase(unittest.TestCase):
    """Ensure Vec2.length returns the vector length."""

    def test_vec2_getitem(self):
        """Ensure vec[0] returns x and vec[1] returns y."""

        a = Vec2(2, 3)

        x = a[0]
        y = a[1]

        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

    def test_vec2_getitem_index_out_of_range(self):
        """Ensure vec[0] returns x and vec[1] returns y."""

        a = Vec2(2, 3)

        index_error_raised = False

        try:
            # Use an index greater than 2.
            a[4]
        except IndexError:
            index_error_raised = True

        self.assertTrue(index_error_raised)


class Vec2DotTestCase(unittest.TestCase):
    """Ensure Vec2.dot returns the dot product."""

    def test_vec2_getitem(self):
        """Ensure Vec2.dot returns the dot product of self and the argument."""

        a = Vec2(2, 3)
        b = Vec2(1, 4)

        result = a.dot(b)

        self.assertEqual(result, 14)


class DotV2TestCase(unittest.TestCase):
    """Ensure dot_v2 returns the dot product."""

    def test_vec2_getitem(self):
        """Ensure dot_v2 returns the dot product of the two vectors."""

        from pedemath.vec2 import dot_v2

        a = Vec2(2, 3)
        b = Vec2(1, 4)

        result = dot_v2(a, b)

        self.assertEqual(result, 14)


class Vec2GetsAndSetsTestCase(unittest.TestCase):
    """Ensure Vec2 get and set functions return the right values."""

    def test_vec2_get_x(self):
        """Ensure get_x returns x."""

        a = Vec2(2, 3)

        self.assertEqual(a.get_x(), 2)

    def test_vec2_set_x(self):
        """Ensure set_x sets Vec2.x."""

        a = Vec2(2, 3)

        a.set_x(5)

        self.assertEqual(a.x, 5)

    def test_vec2_get_y(self):
        """Ensure get_y returns y."""

        a = Vec2(2, 3)

        self.assertEqual(a.get_y(), 3)

    def test_vec2_set_y(self):
        """Ensure set_y sets Vec2.y."""

        a = Vec2(2, 3)

        a.set_y(5)

        self.assertEqual(a.y, 5)

    def test_vec2_set(self):
        """Ensure set() sets Vec2 x and y."""

        a = Vec2(2, 3)

        a.set(7, 8)

        self.assertEqual(a.x, 7)
        self.assertEqual(a.y, 8)


class Vec2RotRadsTestCase(unittest.TestCase):
    """Ensure Vec2.rot_rads rotates the vector."""

    def test_vec2_rot_rads(self):
        """Ensure Vec2.rot_rads rotates the vector correctly."""

        import math

        from collections import namedtuple
        Case = namedtuple('Case', 'start_vector angle expected_result_vec')

        cases = [
            # Start vector, angle to rotate, expected_result_vec
            Case(Vec2(1, 0), 0, Vec2(1, 0)),
            Case(Vec2(1, 0), math.pi / 2, Vec2(0, 1)),
            Case(Vec2(1, 0), math.pi, Vec2(-1, 0)),
            Case(Vec2(1, 0), math.pi * 3 / 2, Vec2(0, -1)),

            Case(Vec2(1, 1), 0, Vec2(1, 1)),
            Case(Vec2(1, 1), math.pi / 2, Vec2(-1, 1)),
            Case(Vec2(1, 1), math.pi, Vec2(-1, -1)),
            Case(Vec2(1, 1), math.pi * 3 / 2, Vec2(1, -1)),

            Case(Vec2(-3, -4), 0, Vec2(-3, -4)),
            Case(Vec2(-3, -4), -math.pi / 2, Vec2(-4, 3)),
            Case(Vec2(-3, -4), -math.pi, Vec2(3, 4)),
            Case(Vec2(-3, -4), -math.pi * 3 / 2, Vec2(4, -3)),
        ]

        for case in cases:
            vec, radians, expected_result_vec = case
            vec.rot_rads(radians)
            self.assertAlmostEqual(vec.x, expected_result_vec.x)
            self.assertAlmostEqual(vec.y, expected_result_vec.y)


class RotRadsV2(unittest.TestCase):
    """Ensure rot_rads_v2 rotates the vector."""

    def test_rot_rads_v2(self):
        """Ensure rot_rads_v2 rotates the vector correctly."""

        import math

        from pedemath.vec2 import rot_rads_v2

        from collections import namedtuple
        Case = namedtuple('Case', 'start_vector angle expected_result_vec')

        cases = [
            # Start vector, angle to rotate, expected_result_vec
            Case(Vec2(1, 0), 0, Vec2(1, 0)),
            Case(Vec2(1, 0), math.pi / 2, Vec2(0, 1)),
            Case(Vec2(1, 0), math.pi, Vec2(-1, 0)),
            Case(Vec2(1, 0), math.pi * 3 / 2, Vec2(0, -1)),

            Case(Vec2(1, 1), 0, Vec2(1, 1)),
            Case(Vec2(1, 1), math.pi / 2, Vec2(-1, 1)),
            Case(Vec2(1, 1), math.pi, Vec2(-1, -1)),
            Case(Vec2(1, 1), math.pi * 3 / 2, Vec2(1, -1)),

            Case(Vec2(-3, -4), 0, Vec2(-3, -4)),
            Case(Vec2(-3, -4), -math.pi / 2, Vec2(-4, 3)),
            Case(Vec2(-3, -4), -math.pi, Vec2(3, 4)),
            Case(Vec2(-3, -4), -math.pi * 3 / 2, Vec2(4, -3)),
        ]

        for case in cases:
            vec, radians, expected_result_vec = case
            result_vec = rot_rads_v2(vec, radians)
            self.assertAlmostEqual(result_vec.x, expected_result_vec.x)
            self.assertAlmostEqual(result_vec.y, expected_result_vec.y)


class AngleV2RadDirTestCase(unittest.TestCase):

    def test_angle_v2_rad_dir(self):
        """Test angle_v2_rad_dir with different cases.
        """
        import math
        from pedemath.vec2 import angle_v2_rad_dir, Vec2

        from collections import namedtuple
        Case = namedtuple('Case', 'vectors expected_result')

        cases = [
            Case((Vec2(1, 0), Vec2(1, 0)), 0),
            Case((Vec2(0, 1), Vec2(0, 1)), 0),
            # clockwise is negative, (-45 degrees)
            Case((Vec2(0, 1), Vec2(1, 1)), -math.pi / 4),
            # counter-clockwise is positive, (45 degrees)
            Case((Vec2(0, 1), Vec2(-1, 1)), math.pi / 4),
            # slightly different angle, 30 degrees
            Case((Vec2(0, 1), Vec2(1.0 / 2, math.sqrt(3) / 2)), -math.pi / 6),
            Case((Vec2(0, 1), Vec2(-1.0 / 2, math.sqrt(3) / 2)), math.pi / 6),
            # simple 45 degrees from different starting vectors
            Case((Vec2(0, -1), Vec2(1, -1)), math.pi / 4),
            Case((Vec2(0, -1), Vec2(-1, -1)), -math.pi / 4),
            Case((Vec2(1, 0), Vec2(1, 1)), math.pi / 4),
            Case((Vec2(1, 0), Vec2(1, -1)), -math.pi / 4),
            Case((Vec2(-1, 0), Vec2(-1, 1)), -math.pi / 4),
            Case((Vec2(-1, 0), Vec2(-1, -1)), math.pi / 4),
            # starting vector is not on axis
            Case((Vec2(1, 1), Vec2(1, 0)), -math.pi / 4),
            Case((Vec2(1, 1), Vec2(0, 1)), math.pi / 4),
            Case((Vec2(-1, 1), Vec2(-1, 0)), math.pi / 4),
            Case((Vec2(-1, 1), Vec2(0, 1)), -math.pi / 4),
            Case((Vec2(-1, -1), Vec2(-1, 0)), -math.pi / 4),
            Case((Vec2(-1, -1), Vec2(0, -1)), math.pi / 4),
            Case((Vec2(1, -1), Vec2(1, 0)), math.pi / 4),
            Case((Vec2(1, -1), Vec2(0, -1)), -math.pi / 4),
            # result vector is larger than 90 degrees
            Case((Vec2(1, 1), Vec2(-1, 0)), math.pi * 3 / 4),
            Case((Vec2(1, 1), Vec2(0, -1)), -math.pi * 3 / 4),
            Case((Vec2(-1, 1), Vec2(1, 0)), -math.pi * 3 / 4),
            Case((Vec2(-1, 1), Vec2(0, -1)), math.pi * 3 / 4),
            Case((Vec2(-1, -1), Vec2(1, 0)), math.pi * 3 / 4),
            Case((Vec2(-1, -1), Vec2(0, 1)), -math.pi * 3 / 4),
            Case((Vec2(1, -1), Vec2(-1, 0)), -math.pi * 3 / 4),
            Case((Vec2(1, -1), Vec2(0, 1)), math.pi * 3 / 4),
            # check what happens at 180 degrees and be consistent
            Case((Vec2(0, 1), Vec2(0, -1)), math.pi),
            Case((Vec2(1, 0), Vec2(-1, 0)), math.pi),
            Case((Vec2(1, 1), Vec2(-1, -1)), math.pi),
            Case((Vec2(-1, 1), Vec2(1, -1)), math.pi),
            Case((Vec2(-1, -1), Vec2(1, 1)), math.pi),
            Case((Vec2(1, -1), Vec2(-1, 1)), math.pi),
        ]

        for case in cases:
            ((vec_a, vec_b), expected_result) = case
            print "TEST:", vec_a, vec_b, "expected:", expected_result
            self.assertAlmostEqual(
                angle_v2_rad_dir(vec_a, vec_b), expected_result,
                places=7)


class RotRadsV2TestCase(unittest.TestCase):

    def test_rot_rads_v2(self):
        import math
        from pedemath.vec2 import rot_rads_v2, Vec2

        from collections import namedtuple
        Case = namedtuple('Case', 'vector radians expected_result')

        cases = [
            Case(Vec2(1, 0), 0, Vec2(1, 0)),
            Case(Vec2(0, 1), 0, Vec2(0, 1)),
            Case(Vec2(0, 1), -math.pi / 4,
                 Vec2(math.sqrt(2) / 2, math.sqrt(2) / 2)),
            Case(Vec2(0, 1), math.pi / 4,
                 Vec2(-math.sqrt(2) / 2, math.sqrt(2) / 2)),
            Case(Vec2(1, 1), math.pi / 2, Vec2(-1, 1)),
            Case(Vec2(-1, 1), math.pi / 2, Vec2(-1, -1)),
            Case(Vec2(-1, -1), math.pi / 2, Vec2(1, -1)),
            Case(Vec2(1, -1), math.pi / 2, Vec2(1, 1)),
            Case(Vec2(1, 1), -math.pi / 2, Vec2(1, -1)),
            Case(Vec2(-1, 1), -math.pi / 2, Vec2(1, 1)),
            Case(Vec2(-1, -1), -math.pi / 2, Vec2(-1, 1)),
            Case(Vec2(1, -1), -math.pi / 2, Vec2(-1, -1)),
        ]
        """
            # clockwise is negative, (-45 degrees)
            # counter-clockwise is positive, (45 degrees)
            Case((Vec2(0, 1), Vec2(-1, 1)), math.pi / 4),
            # slightly different angle, 30 degrees
            Case((Vec2(0, 1), Vec2(1.0 / 2, math.sqrt(3) / 2)), -math.pi / 6),
            Case((Vec2(0, 1), Vec2(-1.0 / 2, math.sqrt(3) / 2)), math.pi / 6),
            # simple 45 degrees from different starting vectors
            Case((Vec2(0, -1), Vec2(1, -1)), math.pi / 4),
            Case((Vec2(0, -1), Vec2(-1, -1)), -math.pi / 4),
            Case((Vec2(1, 0), Vec2(1, 1)), math.pi / 4),
            Case((Vec2(1, 0), Vec2(1, -1)), -math.pi / 4),
            Case((Vec2(-1, 0), Vec2(-1, 1)), -math.pi / 4),
            Case((Vec2(-1, 0), Vec2(-1, -1)), math.pi / 4),
            # starting vector is not on axis
            Case((Vec2(1, 1), Vec2(1, 0)), -math.pi / 4),
            Case((Vec2(1, 1), Vec2(0, 1)), math.pi / 4),
            Case((Vec2(-1, 1), Vec2(-1, 0)), math.pi / 4),
            Case((Vec2(-1, 1), Vec2(0, 1)), -math.pi / 4),
            Case((Vec2(-1, -1), Vec2(-1, 0)), -math.pi / 4),
            Case((Vec2(-1, -1), Vec2(0, -1)), math.pi / 4),
            Case((Vec2(1, -1), Vec2(1, 0)), math.pi / 4),
            Case((Vec2(1, -1), Vec2(0, -1)), -math.pi / 4),
            # result vector is larger than 90 degrees
            Case((Vec2(1, 1), Vec2(-1, 0)), math.pi * 3 / 4),
            Case((Vec2(1, 1), Vec2(0, -1)), -math.pi * 3 / 4),
            Case((Vec2(-1, 1), Vec2(1, 0)), -math.pi * 3 / 4),
            Case((Vec2(-1, 1), Vec2(0, -1)), math.pi * 3 / 4),
            Case((Vec2(-1, -1), Vec2(1, 0)), math.pi * 3 / 4),
            Case((Vec2(-1, -1), Vec2(0, 1)), -math.pi * 3 / 4),
            Case((Vec2(1, -1), Vec2(-1, 0)), -math.pi * 3 / 4),
            Case((Vec2(1, -1), Vec2(0, 1)), math.pi * 3 / 4),
            # check what happens at 180 degrees and be consistent
            Case((Vec2(0, 1), Vec2(0, -1)), math.pi),
            Case((Vec2(1, 0), Vec2(-1, 0)), math.pi),
            Case((Vec2(1, 1), Vec2(-1, -1)), math.pi),
            Case((Vec2(-1, 1), Vec2(1, -1)), math.pi),
            Case((Vec2(-1, -1), Vec2(1, 1)), math.pi),
            Case((Vec2(1, -1), Vec2(-1, 1)), math.pi),
            """

        for case in cases:
            print case
            (vec_a, rads, expected_result) = case
            print "TEST:", vec_a, rads, "expected:", expected_result
            result = rot_rads_v2(vec_a, rads)
            self.assertAlmostEqual(
                result.x, expected_result.x,
                places=7)
            self.assertAlmostEqual(
                result.y, expected_result.y,
                places=7)
