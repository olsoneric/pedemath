
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

from pedemath.vec3 import Vec3


class Vec3InitTestCase(unittest.TestCase):
    """Test Vec3's constructor."""

    def test_members_are_set(self):
        """Ensure the x, y, and z members are set."""

        v = Vec3(5.0, 6.0, 7.0)

        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)
        self.assertEqual(7.0, v.z)

    def test_members_are_set_when_args_are_ints(self):
        """Ensure the x, y, and z members are set.
        Ensure the members have been made float types.
        """

        v = Vec3(5, 6, 7)

        # Assert member values are what we expect.
        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)
        self.assertEqual(7.0, v.z)

        # Assert member values are floats.
        self.assertTrue(isinstance(v.x, float))
        self.assertTrue(isinstance(v.y, float))
        self.assertTrue(isinstance(v.z, float))

    def test_members_are_set_when_args_are_strs(self):
        """Ensure the x, y, and z members are set.
        Ensure the members have been made float types.

        This isn't necessary functionality, but this works with python,
        so ensure this doesn't change without knowing it might break some
        existing code.  Also, don't want to add overhead in the constructor to
        explicitly disable this.
        """

        v = Vec3("5", "6", "7")

        # Assert member values are what we expect.
        self.assertEqual(5.0, v.x)
        self.assertEqual(6.0, v.y)
        self.assertEqual(7.0, v.z)

        # Assert member values are floats.
        self.assertTrue(isinstance(v.x, float))
        self.assertTrue(isinstance(v.y, float))
        self.assertTrue(isinstance(v.z, float))

    def test_members_are_set_when_args_are_invalid(self):
        """Ensure when an arg is invalid that ValueError is raised."""

        self.assertRaises(ValueError, Vec3, "abc", 6, "q")


class Vec3AddTestCase(unittest.TestCase):
    """Test Vec3's __add__() which is used in Vec3 + Vec3."""

    def test_add_with_vec_argument(self):
        """Ensure that adding another vector returns another Vec3 with the
        right values.
        """

        a = Vec3(2, 3, 4)
        b = Vec3(1, 2, 3)

        result = a + b

        expected_result = Vec3(3, 5, 7)

        self.assertEqual(result, expected_result)

    def test_add_with_float_arg(self):
        """Ensure that adding a float returns another Vec3 with the float
        added to x, y, and z.
        """

        a = Vec3(2, 3, 4)
        b = 5.0

        result = a + b

        expected_result = Vec3(7, 8, 9)

        self.assertEqual(result, expected_result)

    def test_add_with_int_arg(self):
        """Ensure that adding a int returns another Vec3 with the int
        added to x and y.
        """

        a = Vec3(2, 3, 4)
        b = 5

        result = a + b

        expected_result = Vec3(7, 8, 9)

        self.assertEqual(result, expected_result)


class AddV3TestCase(unittest.TestCase):
    """Test add_v3(Vec3, Vec3)."""

    def test_add_with_vec_argument(self):
        """Ensure that adding another vector returns another Vec3 with the
        right values.
        """

        from pedemath.vec3 import add_v3

        a = Vec3(2, 3, 4)
        b = Vec3(1, 2, 3)

        result = add_v3(a, b)

        expected_result = Vec3(3, 5, 7)

        self.assertEqual(result, expected_result)

    def test_add_with_float_arg(self):
        """Ensure that adding a float returns another Vec3 with the float
        added to x and y.
        """

        from pedemath.vec3 import add_v3

        a = Vec3(2, 3, 4)
        b = 5.0

        result = add_v3(a, b)

        expected_result = Vec3(7, 8, 9)

        self.assertEqual(result, expected_result)

    def test_add_with_int_arg(self):
        """Ensure that adding a int returns another Vec3 with the int
        added to x and y.
        """

        from pedemath.vec3 import add_v3

        a = Vec3(2, 3, 4)
        b = 5

        result = add_v3(a, b)

        expected_result = Vec3(7, 8, 9)

        self.assertEqual(result, expected_result)


class Vec3IAddTestCase(unittest.TestCase):
    """Test Vec3 += arg"""

    def test_iadd_with_vec_argument(self):
        """Ensure that Vec3.iadd adds x and y components from a vector."""

        a = Vec3(2, 3, 4)
        b = Vec3(1, 2, 3)

        a += b

        expected_result = Vec3(3, 5, 7)

        self.assertEqual(a, expected_result)

    def test_iadd_with_float_argument(self):
        """Ensure that Vec3.iadd adds the float to Vec3 x and y components."""

        a = Vec3(2, 3, 4)
        b = 1.0

        a -= b

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(a, expected_result)

    def test_iadd_with_int_argument(self):
        """Ensure that Vec3.iadd adds the int to Vec3 x and y components."""

        a = Vec3(2, 3, 4)
        b = 1

        a -= b

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(a, expected_result)


class Vec3GetItemTestCase(unittest.TestCase):
    """Test Vec3.__getite__m() for uses such as: vec[1]."""

    def test_getitem(self):
        """Ensure that vec[0], vec[1], and vec[2] return the correct values."""

        vec = Vec3(4, 5, 6)

        self.assertEqual(4, vec[0])
        self.assertEqual(5, vec[1])
        self.assertEqual(6, vec[2])

    def test_getitem_invalid_index(self):
        """Ensure uses like vec[10000] raise the IndexError exception."""

        vec = Vec3(4, 5, 6)

        # Calling vec.__getitem__ directly instead of vec[5] so we can catch
        # the exception.
        self.assertRaises(IndexError, vec.__getitem__, 5)


class Vec3SetItemTestCase(unittest.TestCase):
    """Test Vec3.__setitem() for uses such as: vec[1] = 5."""

    def test_setitem(self):
        """Ensure that we can set values with vec[0], vec[1], and vec[2]."""

        vec = Vec3(4, 5, 6)

        # Set the values with __setitem__
        vec[0] = 14
        vec[1] = 15
        vec[2] = 16

        # Ensure the values got set.
        self.assertEqual(14, vec[0])
        self.assertEqual(15, vec[1])
        self.assertEqual(16, vec[2])

    def test_setitem_invalid_index(self):
        """Ensure uses like vec[10000] = 5 raise the IndexError exception."""

        vec = Vec3(4, 5, 6)

        self.assertRaises(IndexError, vec.__setitem__, 5, 15)
