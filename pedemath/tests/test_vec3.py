
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
