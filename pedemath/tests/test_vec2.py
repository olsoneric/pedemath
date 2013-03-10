
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
