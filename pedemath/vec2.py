
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


from types import FloatType, IntType
import math

VEC2_EPSILON = 0.00000001


def angle_v2_rad(vec_a, vec_b):
    """Returns angle in range [0, PI], does not distinguisch if a is
    left of or right of b.
    """
    # cos(x) = A * B / |A| * |B|
    return math.acos(vec_a.dot(vec_b) / (vec_a.length() * vec_b.length()))


def angle_v2_rad_dir(vec_a, vec_b):
    """Returns angle in range [-PI, PI] which indicates if vec_a is left of
    or right of b.
    vec_a is the base vector that the returned angle will be based off of.
    e.g. if vec_b is to the right (clockwise) of vec_a, the angle will be
    negative.  (note line about angle dir below)
    Added to simpler function above with these suggestions:
    http://www.physicsforums.com/showthread.php?t=559966
    Positive angle is counterclockwise as trig functions expect
    """
    # cos(x) = A * B / |A| * |B|
    rads = math.acos(vec_a.dot(vec_b) / (vec_a.length() * vec_b.length()))
    if vec_a.x * vec_b.y >= vec_a.y * vec_b.x:
        return rads
    else:
        #print "Have: ", rads, "returning:", -rads
        return -rads


def rot_rads_v2(vec_a, rads):
    x = vec_a.x * math.cos(rads) - vec_a.y * math.sin(rads)
    y = vec_a.x * math.sin(rads) + vec_a.y * math.cos(rads)
    return Vec2(x, y)


def sum_v2(vec):
    return vec.x + vec.y


def scale_v2(vec, amount):
    """Return a new Vec2 with x and y from vec and multiplied by amount."""

    return Vec2(vec.x * amount, vec.y * amount)


def normalize_v2(vec):
    """Return a new normalized Vec2 of vec."""

    try:
        return scale_v2(vec, 1.0 / vec.length())
    except ZeroDivisionError:
        # Handle gracefully.  x and y are probably zero
        return Vec2(0.0, 0.0)


def dot_v2(vec1, vec2):
    """Return the dot product of two vectors"""

    return vec1.x * vec2.x + vec1.y * vec2.y


def add_v2(v, w):
    """Add v and w.  Assume the first arg v is a Vec2.
    The second arg w can be a vec2 or a number.
    """
    if type(w) is float or type(w) is int:
        return Vec2(v.x + w, v.y + w)
    else:
        return Vec2(v.x + w.x, v.y + w.y)


def sub_v2 (v,w):
    if type(w) == IntType or type(w) == FloatType:
        return Vec2(v.x-w, v.y - w)
    else:
        return Vec2(v.x-w.x, v.y - w.y)


def projection_v2(v,w):
    # The signed length of the projection of vector v on vector w.
    return dot_v2(v,w)/w.length()


def square_v2(vec):
    """Return a new Vec2 with each component squared."""

    try:
        return Vec2(vec.x ** 2, vec.y ** 2)

    except OverflowError:

        try:
            x = vec.x ** 2
        except:
            x = 0.0

        try:
            y = vec.y ** 2
        except:
            y = 0.0

        return Vec2(x, y)


def cross_v2(obj1, obj2):
    return Vec2(obj1.y*obj2.x-obj1.x*obj2.y,
    obj1.y*obj2.x-obj1.x*obj2.y)


class Vec2:
    def __init__(self, x=0., y=0.):
        """Initialize member variables x and y from args.
        Convert args to float if possible, otherwise ValueError should
        be raised.

        To create from another Vec2 is to use *:
        vec_a = Vec2(3, 2):
        vec_b = Vec2(*vec_a)
        """

        self.x = float(x)
        self.y = float(y)

    def __add__(self, arg):
        """Return a new Vec2 containing the sum of our x and y and arg.

        If argument is a float or vec, add it to our x and y.
        Otherwise, treat is as a Vec2 and add arg.x and arg.y to our own
        x and y.
        """

        # Not using isinstance for now, see spikes/type_check_perf.py
        if type(arg) is float or type(arg) is int:
            return Vec2(self.x + arg, self.y + arg)
        else:
            return Vec2(self.x + arg.x, self.y + arg.y)

    def __neg__(self):
        """Return a Vec2 with -x and -y."""

        return Vec2(-self.x, -self.y)

    def __eq__(self, v2):
        """Return True if x == v2.x and y == 2.y"""

        if self.x == v2.x and self.y == v2.y:
            return True

        return False

    def __ne__(self, v2):
        """Return True if x != v2.x or y != 2.y"""

        if self.x != v2.x or self.y != v2.y:
            return True

        return False

    def normalize(self):
        """Make this vector a unit vector."""

        try:
            self.scale(1.0 / self.length())
        except ZeroDivisionError:
            # Handle gracefully.  x and y are probably zero
            pass

        # Don't return self to help indicate that self is being modified.

    def truncate(self, max_length):
        """Truncate this vector so it's length does not exceed max."""

        if self.length() > max_length:

            # If it's longer than the max_length, scale to the max_length.
            self.scale(max_length / self.length())

        # Don't return self to help indicate that self is being modified.

    def scale(self, amount):
        """Multiply x and y by amount."""

        self.x *= amount
        self.y *= amount

    def square(self):
        """Square the components."""

        # TODO: Look into ** and math.pow more.
        # TODO: Double-check if ** operator will throw OverflowError.
        # If not, remove OverflowError try/excepts.
        try:
            self.x **= 2
        except OverflowError:
            self.x = 0.0

        try:
            self.y **= 2
        except OverflowError:
            self.y = 0.0

    def get_unit_normal(self):
        return self.get_scaled_v2(1.0/self.length())

    def get_scaled_v2(self, amount):
        """Return a new Vec2 with x and y multiplied by amount."""

        return Vec2(self.x * amount, self.y * amount)

    def get_square(self):
        """Return a new Vec2 with x and y that have been squared."""

        try:
            return Vec2(self.x ** 2, self.y ** 2)

        except OverflowError:

            try:
                x = self.x ** 2
            except:
                x = 0.0

            try:
                y = self.y ** 2
            except:
                y = 0.0

            return Vec2(x, y)

    def get_norm(self):
        """Return square length: x*x + y*y."""

        return self.x * self.x + self.y * self.y

    length_squared = get_norm

    def get_perp(self):
        """Return a perpendicular vector."""

        return Vec2(-self.y, self.x)

    def length(self):
        """Return the vector length."""
        return math.sqrt(self.get_norm())

    def __getitem__(self, index):
        """Return x for vec[0] or y for vec[1]."""

        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y

        raise IndexError("Vector index out of range")

    def dot(self, vec):
        """Return the dot product of two vectors."""

        return self.x * vec.x + self.y * vec.y

    def get_y(self):
        return self.y

    def set_y(self, val):
        self.y = val

    def set(self, x, y):
        self.x = x
        self.y = y

    def rot_rads(self, rads):
        self.x = self.x * math.cos(rads) - self.y * math.sin(rads)
        self.y = self.y * math.sin(rads) + self.y * math.cos(rads)

    def __rsub__(self, obj):
        if type(obj) == IntType or type(obj) == FloatType:
            self.x -= obj
            self.y -= obj
        else:
            self.x -= obj.x
            self.y -= obj.y

    def __sub__(self, obj):
        if type(obj) == IntType or type(obj) == FloatType:
            return Vec2(self.x-obj, self.y - obj)
        else:
            return Vec2(self.x-obj.x, self.y - obj.y)

    def __radd__(self, obj):
        self.x += obj.x
        self.y += obj.y

    def __lmul__(self, obj):
        raise "Blah"

    def __mul__(self, obj): # use crossVec2 instead
        return Vec2(self.x * obj, self.y * obj)

    def __div__(self, val):
        return Vec2(self.x / val, self.y / val)

    def __rdiv__(self, val):
        self.x /= val
        self.y /= val

    def __str__(self):
        return str("Vec2(%s,%s)" % (self.x, self.y) )

    __repr__ = __str__

    def __len__(self):
        return 2

if __name__ == "__main__":
    a = Vec2(1, 2)
    print "a:", a
    print "a + 5", a + 5
    print "a * 5", a * 5
    print "a - a", a -a
    b = Vec2(a.x, a.y)
    b -= 5
    print "b -= 5", b
