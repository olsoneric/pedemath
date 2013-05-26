
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

