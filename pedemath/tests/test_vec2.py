
import unittest


class TestVec2(unittest.TestCase):

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
