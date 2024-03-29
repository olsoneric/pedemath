
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


import math
import unittest

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


class Vec3EqualityTestCase(unittest.TestCase):
    """Test Vec3 __eq__ and __ne__. """

    def test_equal_to_vec3(self):
        self.assertEqual(Vec3(1, -2, 3), Vec3(1, -2, 3))

    def test_not_equal_to_vec3(self):
        self.assertNotEqual(Vec3(0, -2, 3), Vec3(1, -2, 3))
        self.assertNotEqual(Vec3(1, 0, 3), Vec3(1, -2, 3))
        self.assertNotEqual(Vec3(1, -2, 0), Vec3(1, -2, 3))

        self.assertNotEqual(Vec3(1, -2, 3), Vec3(0, -2, 3))
        self.assertNotEqual(Vec3(1, -2, 3), Vec3(1, 0, 3))
        self.assertNotEqual(Vec3(1, -2, 3), Vec3(1, -2, 0))

    def test_not_equal_to_other_types(self):
        """When comparing with other types, ensure False is returned and no
        exception is raised.
        """
        from pedemath.quat import Quat

        self.assertNotEqual(Vec3(1, -2, 3), 5)
        self.assertNotEqual(Vec3(1, -2, 3), "abc")

        self.assertNotEqual(Vec3(1, 1, 1), Quat(1, 1, 1, 1))
        self.assertNotEqual(Quat(1, 1, 1, 1), Vec3(1, 1, 1))


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
        """Ensure that Vec3.iadd adds x and y components to a vector."""

        a = Vec3(2, 3, 4)
        b = Vec3(1, 2, 3)

        a += b

        expected_result = Vec3(3, 5, 7)

        self.assertEqual(a, expected_result)

    def test_iadd_with_float_argument(self):
        """Ensure that Vec3.iadd adds the float to Vec3 x and y components."""

        a = Vec3(2, 3, 4)
        b = 1.0

        a += b

        expected_result = Vec3(3, 4, 5)

        self.assertEqual(a, expected_result)

    def test_iadd_with_int_argument(self):
        """Ensure that Vec3.iadd adds the int to Vec3 x and y components."""

        a = Vec3(2, 3, 4)
        b = 1

        a += b

        expected_result = Vec3(3, 4, 5)

        self.assertEqual(a, expected_result)


class Vec3SubTestCase(unittest.TestCase):
    """Test Vec3's __sub__() which is used in Vec3 + Vec3."""

    def test_sub_with_vec_argument(self):
        """Ensure that subtracting another vector returns another Vec3 with the
        right values.
        """

        a = Vec3(2, 4, 6)
        b = Vec3(1, 2, 3)

        result = a - b

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(result, expected_result)

    def test_sub_with_float_arg(self):
        """Ensure that subtracting a float returns another Vec3 with the float
        subtracted from x, y, and z.
        """

        a = Vec3(7, 8, 9)
        b = 5.0

        result = a - b

        expected_result = Vec3(2, 3, 4)

        self.assertEqual(result, expected_result)

    def test_sub_with_int_arg(self):
        """Ensure that subtracting a int returns another Vec3 with the int
        subtracted from x and y.
        """

        a = Vec3(7, 8, 9)
        b = 5

        result = a - b

        expected_result = Vec3(2, 3, 4)

        self.assertEqual(result, expected_result)


class SubV3TestCase(unittest.TestCase):
    """Test sub_v3(Vec3, Vec3)."""

    def test_sub_with_vec_argument(self):
        """Ensure that subtracting another vector returns another Vec3 with the
        right values.
        """

        from pedemath.vec3 import sub_v3

        a = Vec3(2, 4, 6)
        b = Vec3(1, 2, 3)

        result = sub_v3(a, b)

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(result, expected_result)

    def test_sub_with_float_arg(self):
        """Ensure that subtracting a float returns another Vec3 with the float
        subtracted from x and y.
        """

        from pedemath.vec3 import sub_v3

        a = Vec3(7, 8, 9)
        b = 5.0

        result = sub_v3(a, b)

        expected_result = Vec3(2, 3, 4)

        self.assertEqual(result, expected_result)

    def test_sub_with_int_arg(self):
        """Ensure that subtracting a int returns another Vec3 with the int
        subtracted from x and y.
        """

        from pedemath.vec3 import sub_v3

        a = Vec3(7, 8, 9)
        b = 5

        result = sub_v3(a, b)

        expected_result = Vec3(2, 3, 4)

        self.assertEqual(result, expected_result)


class Vec3ISubTestCase(unittest.TestCase):
    """Test Vec3 += arg"""

    def test_isub_with_vec_argument(self):
        """Ensure that Vec3.isub subtracts x, y, and z components from a
        vector.
        """

        a = Vec3(2, 4, 6)
        b = Vec3(1, 2, 3)

        a -= b

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(a, expected_result)

    def test_isub_with_float_argument(self):
        """Ensure that Vec3.isub subtracts the float from Vec3 x, y, and z
        components.
        """

        a = Vec3(2, 3, 4)
        b = 1.0

        a -= b

        expected_result = Vec3(1, 2, 3)

        self.assertEqual(a, expected_result)

    def test_isub_with_int_argument(self):
        """Ensure that Vec3.isub subtracts the int from Vec3 x, y, and z
        components.
        """

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


class Vec3SetTestCase(unittest.TestCase):
    """Test Vec3.set(x, y, z)."""

    def test_setitem(self):
        """Ensure that we can set values with Vec3.set(x, y, z)."""

        vec = Vec3(4, 5, 6)

        # Set the values with .set()
        result = vec.set(7, 8, 9)

        # Ensure the values got set.
        self.assertEqual(Vec3(7, 8, 9), vec)
        # Ensure the object was also returned
        self.assertIs(result, vec)


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


class TestSumV3TestCase(unittest.TestCase):
    """Test sum_v3."""

    def test_sum_v3(self):
        from pedemath.vec3 import sum_v3

        self.assertEqual(8, sum_v3(Vec3(1, 2, 5)))


class TestTranslateV3TestCase(unittest.TestCase):
    """Test translate_v3()."""

    def test_translate_v3(self):
        from pedemath.vec3 import translate_v3

        self.assertEqual(Vec3(3, 4, 7),
                         translate_v3(Vec3(1, 2, 5), 2))


class TestVec3IMulTestCase(unittest.TestCase):
    """Test Vec3().__imul__() and its alias Vec3().scale()."""

    def test_vec3_imul(self):
        """Ensure *= works to scale Vec3() vectors."""

        vec = Vec3(1, 2, 5)

        vec *= 2

        self.assertEqual(Vec3(2, 4, 10), vec)

    def test_vec3_imul_invalid_vector_arg(self):
        """Ensure a type error is raised if imul is used with a vector
        argument.
        """

        vec_a = Vec3(1, 2, 5)

        vec_b = Vec3(5, 6, 7)

        # The next line should raise a TypeError Exception since we should
        # only be able to be able to multiply with numbers, not vectors.
        self.assertRaises(TypeError, vec_a.__imul__, vec_b)

    def test_vec3_scale(self):
        """Ensure Vec3().scale works to scale Vec3() vectors."""

        vec = Vec3(1, 2, 5)

        vec.scale(2)

        self.assertEqual(Vec3(2, 4, 10), vec)


class TestScaleV3TestCase(unittest.TestCase):
    """Test scale_v3()."""

    def test_scale_v3(self):
        from pedemath.vec3 import scale_v3

        self.assertEqual(Vec3(2, 4, 10),
                         scale_v3(Vec3(1, 2, 5), 2))


class TestVec3NormalizeTestCase(unittest.TestCase):
    """Test Vec3().normalize()."""

    def test_vec3_normalize(self):
        from pedemath.vec3 import scale_v3

        vec1 = Vec3(3, 4, 5)
        vec1.normalize()

        expected = scale_v3(Vec3(3, 4, 5), 1.0 / math.sqrt(50))

        self.assertEqual(vec1, expected)


class TestNormalizeV3TestCase(unittest.TestCase):
    """Test normalize_v3()."""

    def test_normalize_v3(self):
        from pedemath.vec3 import normalize_v3
        from pedemath.vec3 import scale_v3

        normalized = normalize_v3(Vec3(3, 4, 5))
        expected = scale_v3(Vec3(3, 4, 5), 1.0 / math.sqrt(50))

        self.assertEqual(normalized, expected)


class TestVec3DotTestCase(unittest.TestCase):
    """Test Vec3().dot()."""

    def test_dot(self):
        """Ensure Vec3.dot() calculates the dotproduct correctly."""

        vec1 = Vec3(3, 4, 5)
        vec2 = Vec3(2, 3, 4)
        dot = vec1.dot(vec2)

        expected = 3 * 2 + 4 * 3 + 5 * 4

        self.assertEqual(dot, expected)


class TestDotV3TestCase(unittest.TestCase):
    """Test dot_v3()."""

    def test_dot_v3(self):
        """Ensure dot_v3 calculates the dotproduct correctly."""

        from pedemath.vec3 import dot_v3

        dot = dot_v3(Vec3(3, 4, 5), Vec3(2, 3, 4))
        expected = 3 * 2 + 4 * 3 + 5 * 4

        self.assertEqual(dot, expected)


class TestVec3CrossTestCase(unittest.TestCase):
    """Test Vec3().cross()."""

    def test_cross_v3(self):
        """Ensure Vec3().cross() calculates the crossproduct correctly."""

        vec1 = Vec3(1, 0, 0)
        vec2 = Vec3(0, 1, 0)
        cross = vec1.cross(vec2)

        expected = Vec3(0, 0, 1)

        self.assertEqual(cross, expected)

    # TODO: add more crossproduct test cases


class TestCrossV3TestCazse(unittest.TestCase):
    """Test cross_v3()."""

    def test_cross_v3(self):
        """Ensure cross_v3 calculates the crossproduct correctly."""

        from pedemath.vec3 import cross_v3

        cross = cross_v3(Vec3(0, -1, 0), Vec3(0, 0, -1))
        expected = Vec3(1, 0, 0)

        self.assertEqual(cross, expected)


class TestVec3UnaryNegativeTestCase(unittest.TestCase):
    """Test unary - with -Vec3()."""

    def test_vec3_unary_negative(self):

        vec = Vec3(3, 4, 5)

        result = -vec

        self.assertEqual(result, Vec3(-3, -4, -5))


class TestNegV3TestCase(unittest.TestCase):
    """Test neg_v3(vec) which acts like unary -."""

    def test_neg_v3(self):
        """Ensure neg_v3(vec), inverts vec's x, y, and z."""

        from pedemath.vec3 import neg_v3

        vec = Vec3(3, 4, 5)

        result = neg_v3(vec)

        self.assertEqual(result, Vec3(-3, -4, -5))


class TestVec3Square(unittest.TestCase):
    """Test Vec3().square() for component-wise squaring of a vector."""

    def test_vec3_square(self):
        """Ensure Vec3().square() squares x, y, and z components."""

        vec = Vec3(2, 3, 4)
        vec.square()

        self.assertEqual(Vec3(4, 9, 16), vec)


class TestSquareV3(unittest.TestCase):
    """Test that square_v3() returns a new vector with squares of the original
    vector's components.
    """

    def test_square_v3(self):
        """Ensure Vec3().square() squares x, y, and z components."""

        from pedemath.vec3 import square_v3

        vec = Vec3(2, 3, 4)
        result_vec = square_v3(vec)

        self.assertEqual(Vec3(4, 9, 16), result_vec)
        # Ensure a new vec was created instead of modifying the original.
        self.assertNotEqual(vec, result_vec)


class TestVec3Str(unittest.TestCase):
    """Test str(Vec3)."""

    def test_vec3_square(self):
        """Ensure str(Vec3()) returns a readable string of the vector."""

        vec = Vec3(2, 3, 4)

        self.assertEqual("Vec3(2.0,3.0,4.0)", str(vec))


class TestVec3Repr(unittest.TestCase):
    """Test repr(Vec3)."""

    def test_vec3_square(self):
        """Ensure repr(Vec3()) returns an unambiguous string of a Vec3."""

        vec = Vec3(2, 3, 4)

        self.assertEqual("Vec3(2.0,3.0,4.0)", repr(vec))


class Vec3AsTupleTestCase(unittest.TestCase):
    """Test Vec3().as_tuple()."""

    def test_as_tuple(self):
        """Ensure that the Vec3's x, y, and z are returned in the tuple."""

        vec = Vec3(7, 8, 9)

        self.assertEqual((7, 8, 9), vec.as_tuple())


class TestProjectionV3TestCase(unittest.TestCase):
    """Test projecting a vector onto another with projection_v3(vec)."""

    def test_projection_v3_x(self):
        """Ensure projection_v3(), correctly returns the resulting length
        of projecting a vector onto another.
        """
        from pedemath.vec3 import projection_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(1, 0, 0)

        result = projection_v3(vec_a, vec_b)

        self.assertEqual(3, result)

    def test_projection_v3_y(self):
        """Ensure projection_v3(), correctly returns the resulting length
        of projecting a vector onto another.
        """
        from pedemath.vec3 import projection_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(0, 1, 0)

        result = projection_v3(vec_a, vec_b)

        self.assertEqual(4, result)

    def test_projection_v3_z(self):
        """Ensure projection_v3(), correctly returns the resulting length
        of projecting a vector onto another.
        """

        from pedemath.vec3 import projection_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(0, 0, 1)

        result = projection_v3(vec_a, vec_b)

        self.assertEqual(5, result)


class TestRotateAroundV3TestCase(unittest.TestCase):
    """Test rotate_around_vector_v3() to rotate a vector around another."""

    def test_rotate_around_v3_z_axis(self):
        """Ensure rotate_around_vector_v3 returns a new vector that has been
        rotated the correct amount.
        """
        from pedemath.vec3 import rotate_around_vector_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(0, 0, 1)

        result = rotate_around_vector_v3(vec_a, math.pi, vec_b)
        expected = Vec3(-3, -4, 5)

        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)
        self.assertAlmostEqual(result.z, expected.z)

    def test_rotate_around_v3_y_axis(self):
        """Ensure rotate_around_vector_v3 returns a new vector that has been
        rotated the correct amount.
        """
        from pedemath.vec3 import rotate_around_vector_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(0, 1, 0)

        result = rotate_around_vector_v3(vec_a, math.pi, vec_b)
        expected = Vec3(-3, 4, -5)

        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)
        self.assertAlmostEqual(result.z, expected.z)

    def test_rotate_around_v3_x_axis(self):
        """Ensure rotate_around_vector_v3 returns a new vector that has been
        rotated the correct amount.
        """
        from pedemath.vec3 import rotate_around_vector_v3

        vec_a = Vec3(3, 4, 5)
        vec_b = Vec3(1, 0, 0)

        result = rotate_around_vector_v3(vec_a, math.pi, vec_b)
        expected = Vec3(3, -4, -5)

        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)
        self.assertAlmostEqual(result.z, expected.z)


class TestAveListV3TestCase(unittest.TestCase):
    """Test getting the average vector from a list of vectors with
    ave_vec3_list().
    """

    def test_ave_list_v3(self):
        """Ensure the average vector from a list of vectors is returned."""

        from pedemath.vec3 import ave_list_v3

        result = ave_list_v3([
            Vec3(3, 6, 9), Vec3(-4, -5, -6), Vec3(4, 5, 6)])

        self.assertEqual(result, Vec3(1, 2, 3))


class TestV3Set(unittest.TestCase):
    """Test Vec3().set(x, y, z)."""

    def test_set_v3(self):
        """Ensure the x, y, and z value are set."""

        test_vec = Vec3(1, 3, 5)
        test_vec.set(2, 4, 6)

        self.assertEqual(test_vec, Vec3(2, 4, 6))
