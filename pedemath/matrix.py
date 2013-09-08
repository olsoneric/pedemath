
import math

from numpy import array, dot

# TODO: see if array is a good replacement for numpy

from pedemath.vec3 import Vec3


class Matrix44(object):
    # C and numarray matrix is in row-major order ( [row][column] )
    # This class will try to return data in column-major order [column][row]

    def __init__(self):
        self.make_identity()

    def make_identity(self):
        """
   #cols[0][0] = 1.0f; cols[1][0] = 0.0f; cols[2][0] = 0.0f; cols[3][0] = 0.0f;
   #cols[0][1] = 0.0f; cols[1][1] = 1.0f; cols[2][1] = 0.0f; cols[3][1] = 0.0f;
   #cols[0][2] = 0.0f; cols[1][2] = 0.0f; cols[2][2] = 1.0f; cols[3][2] = 0.0f;
   #cols[0][3] = 0.0f; cols[1][3] = 0.0f; cols[2][3] = 0.0f; cols[3][3] = 1.0f;
        """

        #self.data = array('f', [[1., 0., 0., 0.],
        #                        [0., 1., 0., 0.],
        #                        [0., 0., 1., 0.],
        #                        [0., 0., 0., 1.]])
        self.data = array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype="float32")

    def __str__(self):
        return str(self.data)

    def __rsub__(self, other):
        if isinstance(other, Matrix44):
            self.data = self.data - other.data
        else:
            raise Exception(
                "Matrix.__rsub__ arg is not a matrix. %s" % type(other))

    def __sub__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = self.data - other.data
            return mat
        else:
            raise Exception(
                "Matrix.__sub__ arg is not a matrix. %s" % type(other))

    def __radd__(self, other):
        if isinstance(other, Matrix44):
            self.data = self.data + other.data
        else:
            raise Exception(
                "Matrix.__sub__ arg is not a matrix. %s" % type(other))

    def __add__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = self.data + other.data
            return mat
        else:
            raise Exception(
                "Matrix.__add__ arg is not a matrix. %s" % type(other))

    def __rmul__(self, other):
        if isinstance(other, Matrix44):
            self.data = dot(self.data, other.data)
        else:
            raise Exception(
                "Matrix44.__rmul__, arg is not a matrix: %s" % type(other))

    def __mul__(self, other):
        if isinstance(other, Matrix44):
            mat = Matrix44()
            mat.data = dot(self.data, other.data)
            return mat
        elif isinstance(other, Vec3):
            v = other
            # just copied from above, delete above checks
            return Vec3(v[0]*self.data[0][0] + v[1] * self.data[1][0] +
                        v[2] * self.data[2][0] + self.data[3][0],
                        v[0] * self.data[0][1] + v[1] * self.data[1][1] +
                        v[2] * self.data[2][1] + self.data[3][1],
                        v[0] * self.data[0][2] + v[1] * self.data[1][2] +
                        v[2] * self.data[2][2] + self.data[3][2])
        else:
            raise Exception("Matrix44.__mul__ unhandled type %s" % type(other))


def matrix44_trans(trans_vec):
    mat = Matrix44()
    # internal data is row major order
    mat.data[3][0] = trans_vec[0]
    mat.data[3][1] = trans_vec[1]
    mat.data[3][2] = trans_vec[2]
    return mat


def matrix44_rot_y(angle_degrees):
    # X^2 * (1-c) + c  |  xy(1-c) -zs     | xz(1-c) +ys     | 0
    # yx(1-c) + zs     |  y^2 * (1-c) +c  | yz(1-c) -xs     | 0
    # xz(1-c) - ys     |  yz(1-c) +xs     | z^2 * (1-c) + z | 0
    # 0                |  0               | 0               | 1
    mat = Matrix44()
    c = math.cos(angle_degrees * math.pi / 180.)
    s = math.sin(angle_degrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[0][0] = c
    mat.data[2][0] = s
    mat.data[0][2] = -s
    mat.data[2][2] = c
    return mat


def matrix44_rot_x(angle_degrees):
    mat = Matrix44()
    c = math.cos(angle_degrees * math.pi / 180.)
    s = math.sin(angle_degrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[1][1] = c
    mat.data[2][1] = -s
    mat.data[1][2] = s
    mat.data[2][2] = c
    return mat


def matrix44_rot_z(angle_degrees):
    mat = Matrix44()
    c = math.cos(angle_degrees * math.pi / 180.)
    s = math.sin(angle_degrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[0][0] = c
    mat.data[1][0] = -s
    mat.data[0][1] = s
    mat.data[1][1] = c
    return mat


def rotate_v3f_deg_xyz(vec_a, rot):
    rot_mat = matrix44_rot_x(rot[0])
    new_vec = rot_mat * vec_a

    rotMat = matrix44_rot_y(rot[1])
    new_vec = rotMat * new_vec

    rot_mat = matrix44_rot_z(rot[2])
    new_vec = rot_mat * new_vec
    return new_vec


if __name__ == "__main__":
    print "Identity:"
    m = Matrix44()
    print m.data

    print "Add:"
    m2 = Matrix44()
    m2.data[0][0] = 5
    m2.data[0][1] = 5
    m2.data[0][2] = 5
    m2.data[0][3] = 5
    print (m + m2).data

    print "Subtract:"
    print (m - m2).data

    print "Multiply:"
    print (m * m2).data

    print "matrix44_trans:"
    m3 = matrix44_trans(Vec3(2, 3, 4))
    print m3.data

    print "matrix44_rot_y:"
    m4 = matrix44_rot_y(45)
    print m4.data

    print "unit x vec rotated by 45:"
    v = Vec3(1, 0, 0)
    print m4 * v

    print "unit x vec rotated by 180:"
    print matrix44_rot_y(180) * v

    print "unit x vec translateed by -5,6,-7:"
    print matrix44_trans(Vec3(-5, 6, -7)) * v

    print "translated and rotated origin:"
    print matrix44_rot_y(45) * matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0)
    print "a:", matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0)
    print "b:", matrix44_rot_y(45) * (
        matrix44_trans(Vec3(1, 0, 0)) * Vec3(0, 0, 0))
    c = matrix44_rot_y(45) * matrix44_trans(Vec3(1, 0, 0))
    print "c:", c
    print "c.5:", c*Vec3(0, 0, 0)
    print "d:", matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0)) * Vec3(1, 0, 0)
    print "e:", matrix44_trans(Vec3(1, 0, 0)) * matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_trans(Vec3(0, 1, 0)) * matrix44_trans(
            Vec3(0, 0, 1))
    print "f:", matrix44_rot_y(45) * Vec3(1, 0, 0)
    print "right:", (matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0))) * Vec3(0, 0, 0)
    print "right 2 (r t i):", (matrix44_rot_y(45) * matrix44_trans(
        Vec3(1, 0, 0))) * Vec3(0, 0, 1)
    print "right 3 (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(45)) * Vec3(0, 0, 1)
    print "      3b (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(45)) * Vec3(0, 0, 1)
    print "correct 4 (t r i):", (matrix44_trans(
        Vec3(1, 0, 0)) * matrix44_rot_y(90)) * Vec3(0, 0, 1)
    print "        4a (t r i):", matrix44_rot_y(90) * Vec3(0, 0, 1)
