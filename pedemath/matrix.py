#from numarray import array, Float32, dot
try:
    from numpy import array, dot
except:
    try:
        from Numeric import array, Float32, dot
        #from numarray import array, Float32, dot
        print "Numpy import failed, trying to use numarray."
    except:
        print "Error Numpy (and Numeric) not available."

from types import InstanceType
import math
from pede3.pmath.vec3 import Vec3

class Matrix44f:
    # C and numarray matrix is in row-major order ( [row][column] )
    # This class will try to return data in column-major order [column][row]

    def __init__(self):
        self.makeIdentity()

    def makeIdentity(self):
        """
    #cols[0][0] = 1.0f; cols[1][0] = 0.0f; cols[2][0] = 0.0f; cols[3][0] = 0.0f;
    #cols[0][1] = 0.0f; cols[1][1] = 1.0f; cols[2][1] = 0.0f; cols[3][1] = 0.0f;
    #cols[0][2] = 0.0f; cols[1][2] = 0.0f; cols[2][2] = 1.0f; cols[3][2] = 0.0f;
    #cols[0][3] = 0.0f; cols[1][3] = 0.0f; cols[2][3] = 0.0f; cols[3][3] = 1.0f;
        """

        self.data = array( [[1,0,0,0],
                            [0,1,0,0],
                            [0,0,1,0],
                            [0,0,0,1]], dtype="float32")

    def __str__(self):
        return str(self.data)

    def __rsub__(self, other):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                self.data = self.data - obj.data
            else:
                raise
        else:
            raise

    def __sub__(self, obj):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                mat = Matrix44f()
                mat.data = self.data - obj.data
                return mat
            else:
                raise
        else:
            raise

    def __radd__(self, other):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                self.data = self.data + obj.data
            else:
                raise
        else:
            raise

    def __add__(self, obj):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                mat = Matrix44f()
                mat.data = self.data + obj.data
                return mat
            else:
                raise
        else:
            raise


    def __rmul__(self, obj):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                self.data = dot(self.data, obj.data)
            else:
                raise
        else:
            raise Exception("Multiplying: %s %s", self.__class__.__name__, type(obj))

    def __mul__(self, obj):
        if type(obj) == Matrix44f:
                mat = Matrix44f()
                mat.data = dot(self.data , obj.data)
                return mat
        elif type(obj) == Vec3:
                v = obj
                # just copied from above, delete above checks 
                return Vec3(v[0]*self.data[0][0] + v[1] * self.data[1][0] + v[2] * self.data[2][0] + self.data[3][0],
                  v[0] * self.data[0][1] + v[1] * self.data[1][1] + v[2] * self.data[2][1] + self.data[3][1],
                   v[0] * self.data[0][2] + v[1] * self.data[1][2] + v[2] * self.data[2][2] + self.data[3][2])
        # older python checks for InstanceType
        elif type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                mat = Matrix44f()
                mat.data = dot(self.data , obj.data)
                return mat
            elif obj.__class__ == Vec3:
                v = obj
                return Vec3(v[0]*self.data[0][0] + v[1] * self.data[1][0] + v[2] * self.data[2][0] + self.data[3][0],
                  v[0] * self.data[0][1] + v[1] * self.data[1][1] + v[2] * self.data[2][1] + self.data[3][1],
                   v[0] * self.data[0][2] + v[1] * self.data[1][2] + v[2] * self.data[2][2] + self.data[3][2])
            else:
                raise Exception("Multiplying: %s %s", self.__class__.__name__, obj.__class__.__name__)
        else:
            raise Exception("Matrix44f, unhandled type %s" % type(obj))

    """
    def __rdiv__(self, other):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                self.data = self.data / obj.data
            else:
                raise
        else:
            raise

    def __div__(self, obj):
        if type(obj) == InstanceType:
            if obj.__class__ == self.__class__:
                mat = Matrix44f()
                mat.data = self.data / obj.data
                return mat
            else:
                raise
        else:
            raise
    """

def Matrix44fTrans(transVec):
    mat = Matrix44f()
    # internal data is row major order
    mat.data[3][0] = transVec[0]
    mat.data[3][1] = transVec[1]
    mat.data[3][2] = transVec[2]
    return  mat

def Matrix44fRotY(angleDegrees):
    # X^2 * (1-c) + c  |  xy(1-c) -zs     | xz(1-c) +ys     | 0
    # yx(1-c) + zs     |  y^2 * (1-c) +c  | yz(1-c) -xs     | 0
    # xz(1-c) - ys     |  yz(1-c) +xs     | z^2 * (1-c) + z | 0
    # 0                |  0               | 0               | 1
    mat = Matrix44f()
    c = math.cos(angleDegrees * math.pi / 180.)
    s = math.sin(angleDegrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[0][0] = c
    mat.data[2][0] = s
    mat.data[0][2] = -s
    mat.data[2][2] = c
    return mat

def Matrix44fRotX(angleDegrees):
    mat = Matrix44f()
    c = math.cos(angleDegrees * math.pi / 180.)
    s = math.sin(angleDegrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[1][1] = c
    mat.data[2][1] = -s
    mat.data[1][2] = s
    mat.data[2][2] = c
    return mat

def Matrix44fRotZ(angleDegrees):
    mat = Matrix44f()
    c = math.cos(angleDegrees * math.pi / 180.)
    s = math.sin(angleDegrees * math.pi / 180.)
    #       row, column for internal storage
    mat.data[0][0] = c
    mat.data[1][0] = -s
    mat.data[0][1] = s
    mat.data[1][1] = c
    return mat

def rotateV3fDegXYZ(vecA, rot):
    rotMat = Matrix44fRotX(rot[0])
    newVec = rotMat * vecA

    rotMat = Matrix44fRotY(rot[1])
    newVec = rotMat * newVec

    rotMat = Matrix44fRotZ(rot[2])
    newVec = rotMat * newVec
    return newVec




if __name__ == "__main__":
    print "Identity:"
    m = Matrix44f()
    print m.data

    print "Add:"
    m2 = Matrix44f()
    m2.data[0][0] = 5
    m2.data[0][1] = 5
    m2.data[0][2] = 5
    m2.data[0][3] = 5
    print (m + m2).data

    print "Subtract:"
    print (m - m2).data

    print "Multiply:"
    print (m * m2).data

    #print "Divide:"
    #m2 = Matrix44f()
    #print (m / m2).data


    print "Matrix44fTrans:"
    m3 = Matrix44fTrans(Vec3(2,3,4))
    print m3.data

    print "Matrix44fRotY:"
    m4 = Matrix44fRotY(45)
    print m4.data

   
    print "unit x vec rotated by 45:"
    v = Vec3(1,0,0)
    print m4 * v

    print "unit x vec rotated by 180:"
    print Matrix44fRotY(180) * v

    print "unit x vec translateed by -5,6,-7:"
    print Matrix44fTrans(Vec3(-5,6,-7)) * v

    print "translated and rotated origin:"
    print Matrix44fRotY(45) * Matrix44fTrans(Vec3(1,0,0)) * Vec3(0,0,0)
    print "a:",Matrix44fTrans(Vec3(1,0,0)) * Vec3(0,0,0)
    print "b:",Matrix44fRotY(45) * (Matrix44fTrans(Vec3(1,0,0)) * Vec3(0,0,0))
    c=Matrix44fRotY(45) * Matrix44fTrans(Vec3(1,0,0))
    print "c:",c
    print "c.5:",c*Vec3(0,0,0)
    print "d:",Matrix44fRotY(45) * Matrix44fTrans(Vec3(1,0,0)) * Vec3(1,0,0)
    print "e:",Matrix44fTrans(Vec3(1,0,0)) * Matrix44fTrans(Vec3(1,0,0)) * Matrix44fTrans(Vec3(0,1,0)) * Matrix44fTrans(Vec3(0,0,1))
    print "f:",Matrix44fRotY(45) * Vec3(1,0,0)
    print "right:", (Matrix44fRotY(45) * Matrix44fTrans(Vec3(1,0,0))) * Vec3(0,0,0)
    print "right 2 (r t i):", (Matrix44fRotY(45) * Matrix44fTrans(Vec3(1,0,0))) * Vec3(0,0,1)
    print "right 3 (t r i):", (Matrix44fTrans(Vec3(1,0,0)) * Matrix44fRotY(45) ) * Vec3(0,0,1)
    print "      3b (t r i):", (Matrix44fTrans(Vec3(1,0,0)) * Matrix44fRotY(45) ) * Vec3(0,0,1)
    print "correct 4 (t r i):", (Matrix44fTrans(Vec3(1,0,0)) * Matrix44fRotY(90) ) * Vec3(0,0,1)
    print "        4a (t r i):", Matrix44fRotY(90)  * Vec3(0,0,1)


