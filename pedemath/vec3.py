
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


def add_v3(vec1, m):
    """Return a new Vec3 containing the sum of our x, y, z, and arg.

    If argument is a float or vec, addt it to our x, y, and z.
    Otherwise, treat it as a Vec3 and add arg.x, arg.y, and arg.z from
    our own x,  y, and z.
    """
    if type(m) is float or type(m) is int:
        return Vec3(vec1.x + m, vec1.y + m, vec1.z + m)
    else:
        return Vec3(vec1.x + m.x, vec1.y + m.y, vec1.z + m.z)


def sub_v3(vec1, m):
    """Return a new Vec3 containing the difference between our x, y, z,
    and m.

    If argument is a float or vec, subtract it from our x, y, and z.
    Otherwise, treat it as a Vec3 and subtract arg.x, arg.y, and arg.z from
    our own x,  y, and z.
    """
    if type(m) is float or type(m) is int:
        return Vec3(vec1.x - m, vec1.y - m, vec1.z - m)
    else:
        return Vec3(vec1.x - m.x, vec1.y - m.y, vec1.z - m.z)


def sum_v3(vec):
    """Return the sum of components x, y, and z."""

    return vec.x + vec.y + vec.z


def translate_v3(vec, amount):
    """Return a new Vec3 that is translated version of vec."""

    return Vec3(vec.x+amount, vec.y+amount, vec.z+amount)


def scale_v3(vec, amount):
    """Return a new Vec3 that is a scaled version of vec."""

    return Vec3(vec.x*amount, vec.y*amount, vec.z*amount)


def normalize_v3(vec):
    """Return a new Vec3 that is normalized version of vec."""

    return scale_v3(vec, 1.0/vec.length())


def dot_v3(v, w):
    """Return the dotproduct of two vectors."""

    return sum([x * y for x, y in zip(v, w)])


def neg_v3(v):
    """Return new Vec3 with -x, -y, and -z."""

    return Vec3(-v.x, -v.y, -v.z)


def projection_v3(v, w):
    """Return the signed length of the projection of vector v on vector w.

    Since the resulting vector is along the 1st vector, you can get the
    full vector result by scaling the 1st vector to the length of the result of
    this function.
    """
    return dot_v3(v, w) / w.length()


def cross_v3(obj1, obj2):
    return Vec3(obj1.y * obj2.z - obj1.z * obj2.y,
                obj1.z * obj2.x - obj1.x * obj2.z,
                obj1.x * obj2.y - obj1.y * obj2.x)


def square_v3(vec):
    return Vec3(vec.x**2, vec.y**2, vec.z**2)


def rotate_around_vector_v3(v, angle_rad, norm_vec):
    """ rotate v around norm_vec by angle_rad."""
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)
    ## (v * cosVal) +
    ## ((normVec * v) * (1.0 - cosVal)) * normVec +
    ## (v ^ normVec) * sinVal)
    #line1: scaleV3(v,cosVal)
    #line2: dotV3( scaleV3( dotV3(normVec,v), 1.0-cosVal), normVec)
    #line3: scaleV3( crossV3( v,normVec), sinVal)
    #a = scaleV3(v,cosVal)
    #b = scaleV3( normVec, dotV3(normVec,v) * (1.0-cosVal))
    #c = scaleV3( crossV3( v,normVec), sinVal)
    return add_v3(
        add_v3(scale_v3(v, cos_val),
               scale_v3(norm_vec, dot_v3(norm_vec, v) * (1.0 - cos_val))),
        scale_v3(cross_v3(v, norm_vec), sin_val)
    )


def ave_vec3_list(vec_list):
    vec = Vec3(0, 0, 0)
    for v in vec_list:
        vec += v
    num_vecs = float(len(vec_list))
    vec = (vec.x / num_vecs, vec.y / num_vecs, vec.z / num_vecs)
    return vec


class Vec3(object):

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        """Initialize member variables x, y, and z from args.
        Convert args to float if possible, otherwise ValueError should
        be raised.

        To create from another Vec2 is to use *:
        vec_a = Vec2(3, 2, 4):
        vec_b = Vec2(*vec_a)
        """

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, m):
        """Return a new Vec3 containing the sum of our x, y, z, and m.

        If the argument m is a float or vec, add it to our x, y, and z.
        Otherwise, treat it as a Vec3 and add m.x, m.y, and m.z to our
        own x, y, and z.
        """

        # Not using isinstance for now, see spikes/type_check_perf.py
        if type(m) is float or type(m) is int:
            return Vec3(self.x + m, self.y + m, self.z + m)
        else:
            return Vec3(self.x + m.x, self.y + m.y, self.z + m.z)

    def __sub__(self, m):
        """Return a new Vec3 containing the difference between our x, y, z,
        and m.

        If the argument m is a float or vec, subtract it from our x, y, and z.
        Otherwise, treat it as a Vec3 and subtract m.x, m.y, and m.z from
        our own x, y, and z.
        """

        # Not using isinstance for now, see spikes/type_check_perf.py
        if type(m) is float or type(m) is int:
            return Vec3(self.x - m, self.y - m, self.z - m)
        else:
            return Vec3(self.x - m.x, self.y - m.y, self.z - m.z)

    def __getitem__(self, index):
        """Return the value at index.
        For example, at index 0, return x.
        Raise IndexError if index is invalid.
        """

        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y
        elif (index == 2):
            return self.z

        raise IndexError("Vector index out of range")

    def __setitem__(self, index, value):
        """Set the value at the index.
        For example, at index 0, set x to value.
        Return the value that is set.
        Raise IndexError if index is invalid.
        """

        if (index == 0):
            self.x = value
            return self.x
        elif (index == 1):
            self.y = value
            return self.y
        elif (index == 2):
            self.z = value
            return self.z

        raise IndexError("Vector index out of range")

    def __len__(self):
        return 3

    def get_norm(self):
        """Return the square length: x^2 + y^2 + z^2"""
        return sum_v3(square_v3(self))

    def length(self):
        return math.sqrt(self.get_norm())

    length_squared = get_norm

    def __str__(self):
        return str("vec3(%s,%s,%s)" % (self.x, self.y, self.z))

    def __repr__(self):
        return str("vec3(%s,%s,%s)" % (self.x, self.y, self.z))

    def __eq__(self, v2):
        return (
            hasattr(v2, "x") and
            self.x == v2.x and self.y == v2.y and self.z == v2.z)

    def __ne__(self, v2):
        return not (
            hasattr(v2, "x") and
            self.x == v2.x and self.y == v2.y and self.z == v2.z)

    def __neg__(self):
        """Return new Vec3 with -x, -y, and -z."""

        return Vec3(-self.x, -self.y, -self.z)

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def dot(self, w):
        """Return the dotproduct between self and another vector."""

        return sum([x * y for x, y in zip(self, w)])

    def cross(self, obj2):
        return Vec3(self.y * obj2.z - self.z * obj2.y,
                    self.z * obj2.x - self.x * obj2.z,
                    self.x * obj2.y - self.y * obj2.x)

    def square(self):
        """ square the components """

        self.x **= 2
        self.y **= 2
        self.z **= 2

    def normalize(self):
        """Normalize in place."""

        return self.scale(1.0 / self.length())

    def get_data_ptr(self):  # mostly for compatibility with old particle code
        return (self.x, self.y, self.z)

    def __iadd__(self, arg):
        """Add arg, +=.

        If argument is a float or vec, subtract it from our x, y, and z.
        Otherwise, treat is as a Vec3 and subtract arg.x, arg.y, and arg.z from
        our own x and y.
        """

        if type(arg) is float or type(arg) is int:
            self.x += arg
            self.y += arg
            self.z += arg
        else:
            self.x += arg.x
            self.y += arg.y
            self.z += arg.z
        return self

    def __isub__(self, v2):
        if hasattr(v2, "x"):
            self.x -= v2.x
            self.y -= v2.y
            self.z -= v2.z
        else:
            self.x -= v2
            self.y -= v2
            self.z -= v2
        return self

    def __imul__(self, v2):
        if hasattr(v2, "x"):
            self.x *= v2.x
            self.y *= v2.y
            self.z *= v2.z
        else:
            self.x *= v2
            self.y *= v2
            self.z *= v2
        return self

    scale = __imul__

    translate = __iadd__
