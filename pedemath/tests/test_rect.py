
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

from pedemath.rect import Rect


class RectInitTestCase(unittest.TestCase):
    """Test Rect's constructor."""

    def test_members_are_set(self):
        """Ensure the x and y members are set."""

        rect = Rect(5, 6, 10, 11)

        self.assertEqual(5, rect.x)
        self.assertEqual(6, rect.y)
        self.assertEqual(10, rect.width)
        self.assertEqual(11, rect.height)


class RectCollidePointTestCase(unittest.TestCase):
    """Test Rect.collidepoint."""

    def test_when_point_is_in(self):
        """Ensure True is returned when the point is in the rect."""

        rect = Rect(5, 6, 10, 11)

        self.assertTrue(rect.collidepoint((8, 8)))

    def test_when_point_is_in_with_nonoverlapping_x_and_y_ranges(self):
        """Ensure True is returned when the point is in the rect.
        Test with x range is not overlapping with the y range.
        """

        rect = Rect(2, 50, 10, 10)

        self.assertTrue(rect.collidepoint((8, 55)))

    def test_when_point_is_left(self):
        """Ensure False is returned when the point is left of rect."""

        rect = Rect(2, 50, 10, 10)

        self.assertFalse(rect.collidepoint((0, 55)))

    def test_when_point_is_right(self):
        """Ensure False is returned when the point is right of rect."""

        rect = Rect(2, 50, 10, 10)

        self.assertFalse(rect.collidepoint((13, 55)))

    def test_when_point_is_below(self):
        """Ensure False is returned when the point is below rect."""

        rect = Rect(2, 50, 10, 10)

        self.assertFalse(rect.collidepoint((8, 49)))

    def test_when_point_is_above(self):
        """Ensure False is returned when the point is above rect."""

        rect = Rect(2, 50, 10, 10)

        self.assertFalse(rect.collidepoint((8, 65)))

