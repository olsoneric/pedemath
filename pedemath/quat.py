import logging
import math

from pedemath.matrix import Matrix44
from pedemath.vec3 import add_v3
from pedemath.vec3 import normalize_v3
from pedemath.vec3 import scale_v3
from pedemath.vec3 import Vec3


def invert_quat(quat):
    length = quat.length()
    return Quat(
        -quat.x / length, -quat.y / length, -quat.z / length, quat.w / length)


def conjugate_quat(quat):
    """Negate the vector part of the quaternion."""
    return Quat(-quat.x, -quat.y, -quat.z, quat.w)


def dot_quat(quat1, quat2):
    return (quat1.x * quat2.x + quat1.y * quat2.y + quat1.z * quat2.z +
            quat1.w * quat2.w)


def lerp_quat(from_quat, to_quat, percent):
    """Return linear interpolation of two quaternions."""

    # Check if signs need to be reversed.
    if dot_quat(from_quat, to_quat) < 0.0:
        to_sign = -1
    else:
        to_sign = 1

    # Simple linear interpolation
    percent_from = 1.0 - percent
    percent_to = percent

    result = Quat(
        percent_from * from_quat.x + to_sign * percent_to * to_quat.x,
        percent_from * from_quat.y + to_sign * percent_to * to_quat.y,
        percent_from * from_quat.z + to_sign * percent_to * to_quat.z,
        percent_from * from_quat.w + to_sign * percent_to * to_quat.w)

    return result


def nlerp_quat(from_quat, to_quat, percent):
    """Return normalized linear interpolation of two quaternions.

    Less computationally expensive than slerp (which not implemented in this
    lib yet), but does not maintain a constant velocity like slerp.
    """

    result = lerp_quat(from_quat, to_quat, percent)
    result.normalize()
    return result


class Quat(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    @staticmethod
    def from_quat(q):
        return Quat(q.x, q.y, q.z, q.w)

    def make_ident(self):

        self.x = float(0)
        self.y = float(0)
        self.z = float(0)
        self.w = float(1)

    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def is_ident(self):
        return (self.x == 0.0 and self.y == 0.0 and self.z == 0.0 and
                self.w == 1.0)

    def __eq__(self, quat):
        if not isinstance(quat, Quat):
            return False

        return (self.x == quat.x and self.y == quat.y and self.z == quat.z and
                self.w == quat.w)

    def __ne__(self, quat):
        """Not equal operator.

        Keep this function to keep compatibility with python2 for now.  Remove
        this function in the future.
        """
        return not self.__eq__(quat)

    def __str__(self):
        """Return a readable string representation of Quat."""
        return str("Quat(%s,%s,%s,%s)" % (self.x, self.y, self.z, self.w))

    def __repr__(self):
        """Return an unambiguous string representation of Quat."""
        return str("Quat(%s,%s,%s,%s)" % (self.x, self.y, self.z, self.w))

    def __mul__(self, quat1):
        x = (self.w * quat1.x + self.x * quat1.w + self.y * quat1.z - self.z *
             quat1.y)
        y = (self.w * quat1.y - self.x * quat1.z + self.y * quat1.w + self.z *
             quat1.x)
        z = (self.w * quat1.z + self.x * quat1.y - self.y * quat1.x + self.z *
             quat1.w)
        w = (self.w * quat1.w - self.x * quat1.x - self.y * quat1.y - self.z *
             quat1.z)
        return Quat(x, y, z, w)

    def __imul__(self, quat1):
        """Multiply arg m with self (*=) and store the result on self."""

        x = (self.w * quat1.x + self.x * quat1.w + self.y * quat1.z - self.z *
             quat1.y)
        y = (self.w * quat1.y - self.x * quat1.z + self.y * quat1.w + self.z *
             quat1.x)
        z = (self.w * quat1.z + self.x * quat1.y - self.y * quat1.x + self.z *
             quat1.w)
        w = (self.w * quat1.w - self.x * quat1.x - self.y * quat1.y - self.z *
             quat1.z)

        self.x, self.y, self.z, self.w = x, y, z, w

        return self

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z +
                         self.w * self.w)

    def dot(self, quat):
        return (self.x * quat.x + self.y * quat.y + self.z * quat.z +
                self.w * quat.w)

    def normalize(self):
        length = self.length()
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length
        self.w = self.w / length

    def invert(self):
        length = self.length()
        self.x = -self.x / length
        self.y = -self.y / length
        self.z = -self.z / length
        self.w = self.w / length

    def conjugate(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

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
        elif (index == 3):
            return self.w

        raise IndexError("Quat index out of range %s" % index)

    def rotate_vec(self, vec):
        """
        https://code.google.com/p/kri/wiki/Quaternions
        v + 2.0*cross(q.xyz, cross(q.xyz,v) + q.w*v);
        """
        xyz = Vec3(self.x, self.y, self.z)
        return add_v3(vec, scale_v3(
            xyz.cross(xyz.cross(vec) + scale_v3(vec, self.w)), 2.0))

    def to_euler_rad(self, dst_euler_vec3=None):
        """Returns euler angles

        dst_euler_vec3 is an optional destination vector.
        """

        euler_vec3 = dst_euler_vec3 or Vec3(0.0, 0.0, 0.0)

        # TODO consolidated duplicated code in this function and to_euler_deg()
        sqw = self.w * self.w
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z

        euler_vec3.z = math.atan2(2.0 * (self.x * self.y + self.z * self.w),
                                  (sqx - sqy - sqz + sqw))
        euler_vec3.x = math.atan2(2.0 * (self.y * self.z + self.x * self.w),
                                  (-sqx - sqy + sqz + sqw))
        euler_vec3.y = math.asin(-2.0 * (self.x * self.z - self.y * self.w))
        return euler_vec3

    def to_euler_deg(self, euler_vec3):
        """Returns euler angles"""
        sqw = self.w * self.w
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z

        euler_vec3.z = math.atan2(2.0 * (self.x * self.y + self.z * self.w),
                                  (sqx - sqy - sqz + sqw)
                                  ) * (180.0 / math.pi)
        euler_vec3.x = math.atan2(2.0 * (self.y * self.z + self.x * self.w),
                                  (-sqx - sqy + sqz + sqw)
                                  ) * (180.0 / math.pi)
        euler_vec3.y = math.asin(-2.0 * (self.x * self.z - self.y * self.w)
                                 ) * (180.0 / math.pi)
        return euler_vec3

    def get_y_rot_rads(self):
        return math.asin(-2.0 * (self.x * self.z - self.y * self.w))

    def get_y_rot_deg(self):
        return self.get_y_rot_rads() * 180.0 / math.pi

    @staticmethod
    def from_axis_angle(axis_v3, angle_deg):

        axis_v3 = normalize_v3(axis_v3)

        angle_rad = angle_deg * math.pi / 180.

        quat = Quat(math.sin(angle_rad / 2.0) * axis_v3[0],
                    math.sin(angle_rad / 2.0) * axis_v3[1],
                    math.sin(angle_rad / 2.0) * axis_v3[2],
                    math.cos(angle_rad / 2.0))

        return quat

    def as_matrix44(self, matrix=None):

        if not matrix:
            matrix = Matrix44()

        matrix.data[0][0] = 1.0 - 2.0 * self.y * self.y - 2.0 * self.z * self.z
        matrix.data[1][0] = 2.0 * self.x * self.y - 2.0 * self.z * self.w
        matrix.data[2][0] = 2.0 * self.x * self.z + 2.0 * self.y * self.w
        matrix.data[3][0] = 0.0

        matrix.data[0][1] = 2.0 * self.x * self.y + 2.0 * self.z * self.w
        matrix.data[1][1] = 1.0 - 2.0 * self.x * self.x - 2.0 * self.z * self.z
        matrix.data[2][1] = 2.0 * self.y * self.z - 2.0 * self.x * self.w
        matrix.data[3][1] = 0.0

        matrix.data[0][2] = 2.0 * self.x * self.z - 2.0 * self.y * self.w
        matrix.data[1][2] = 2.0 * self.y * self.z + 2.0 * self.x * self.w
        matrix.data[2][2] = 1.0 - 2.0 * self.x * self.x - 2.0 * self.y * self.y
        matrix.data[3][2] = 0.0

        matrix.data[0][3] = 0.0
        matrix.data[1][3] = 0.0
        matrix.data[2][3] = 0.0
        matrix.data[3][3] = 1.0

        return matrix

    def get_rot_matrix(self):
        logging.warning("Use as_rot_matrix44() instead of get_rot_matrix().")
        return self.as_matrix44()

    @classmethod
    def from_matrix44(quat_cls, mat):
        quat = quat_cls()
        quat.set_from_matrix44(mat)
        return quat

    def set_from_matrix44(self, mat):
        """Create a new Quat from a Matrix44.

        Note that the matrix and indexes are column major.
        """

        # Matrix trace
        trace = mat.data[0][0] + mat.data[1][1] + mat.data[2][2] + 1.0

        if trace > 0.00000001:
            # n4 is norm of quaternion multiplied by 4.
            n4 = math.sqrt(trace) * 2
            self.x = (mat.data[1][2] - mat.data[2][1]) / n4
            self.y = (mat.data[2][0] - mat.data[0][2]) / n4
            self.z = (mat.data[0][1] - mat.data[1][0]) / n4
            self.w = n4 / 4.0
            return self

        # TODO: unittests for code below when trace is small.

        # matrix trace <= 0
        if mat.data[0][0] > mat.data[1][1] and mat.data[0][0] > mat.data[2][2]:
            s = 2.0 * math.sqrt(1.0 + mat.data[0][0] - mat.data[1][1] -
                                mat.data[2][2])
            self.x = s / 4.0
            self.y = (mat.data[1][0] + mat.data[0][1]) / s
            self.z = (mat.data[2][0] + mat.data[0][2]) / s
            self.w = (mat.data[2][1] - mat.data[1][2]) / s
            return self
        elif mat.data[1][1] > mat.data[2][2]:
            s = 2.0 * math.sqrt(1.0 - mat.data[0][0] + mat.data[1][1] -
                                mat.data[2][2])
            self.x = (mat.data[1][0] + mat.data[0][1]) / s
            self.y = s / 4.0
            self.z = (mat.data[2][1] + mat.data[1][2]) / s
            self.w = (mat.data[2][0] - mat.data[0][2]) / s
            return self
        else:
            s = 2.0 * math.sqrt(1.0 - mat.data[0][0] - mat.data[1][1] +
                                mat.data[2][2])
            self.x = (mat.data[2][0] + mat.data[0][2]) / s
            self.y = (mat.data[2][1] + mat.data[1][2]) / s
            self.z = s / 4.0
            self.w = (mat.data[1][0] - mat.data[0][1]) / s
            return self

    # @classmethod
    # def from_matrix44(cls, mat):
    #     """Create a new Quat from a Matrix44.

    #     Note that the matrix and indexes are column major.
    #     """

    #     # Matrix trace
    #     trace = mat.data[0][0] + mat.data[1][1] + mat.data[2][2] + 1.0

    #     if trace > 0.00000001:
    #         # n4 is norm of quaternion multiplied by 4.
    #         n4 = math.sqrt(trace) * 2
    #         return Quat((mat.data[1][2] - mat.data[2][1]) / n4,  # x
    #                     (mat.data[2][0] - mat.data[0][2]) / n4,  # y
    #                     (mat.data[0][1] - mat.data[1][0]) / n4,  # z
    #                     n4 / 4.0)                                # w

    #     # TODO: unittests for code below when trace is small.

    #     # matrix trace <= 0
    #     if mat.data[0][0] > mat.data[1][1] and (
    #             mat.data[0][0] > mat.data[2][2]):
    #         s = 2.0 * math.sqrt(1.0 + mat.data[0][0] - mat.data[1][1] -
    #                             mat.data[2][2])
    #         return Quat(s / 4.0,                              # x
    #                     (mat.data[1][0] + mat.data[0][1]) / s,  # y
    #                     (mat.data[2][0] + mat.data[0][2]) / s,  # z
    #                     (mat.data[2][1] - mat.data[1][2]) / s)  # w
    #     elif mat.data[1][1] > mat.data[2][2]:
    #         s = 2.0 * math.sqrt(1.0 - mat.data[0][0] + mat.data[1][1] -
    #                             mat.data[2][2])
    #         return Quat((mat.data[1][0] + mat.data[0][1]) / s,  # x
    #                     s / 4.0,                              # y
    #                     (mat.data[2][1] + mat.data[1][2]) / s,  # z
    #                     (mat.data[2][0] - mat.data[0][2]) / s)  # w
    #     else:
    #         s = 2.0 * math.sqrt(1.0 - mat.data[0][0] - mat.data[1][1] +
    #                             mat.data[2][2])
    #         return Quat((mat.data[2][0] + mat.data[0][2]) / s,  # x
    #                     (mat.data[2][1] + mat.data[1][2]) / s,  # y
    #                     s / 4.0,                              # z
    #                     (mat.data[1][0] - mat.data[0][1]) / s)  # w
