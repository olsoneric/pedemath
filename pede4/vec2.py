from types import InstanceType, FloatType, IntType
import math

Vec2Epsilon = 0.00000001

def angleV2Rad(vecA, vecB):
    # cos(x) = A * B / |A| * |B|
    return math.acos(vecA.dot(vecB) / (vecA.length() * vecB.length()))

def sumV2(vec):
    return vec.x + vec.y

def scaleV2(vec, amount):
    return Vec2(vec.x*amount, vec.y*amount)

def normalizeV2(vec):
    try:
        return scaleV2(vec, 1.0/vec.length())
    except ZeroDivisionError:
        return Vec2(0.0, 0.0)

def dotV2 (v,w):
    # The dot product of two vectors
    return sum( [ x*y for x,y in zip(v,w) ] )

def addV2 (v,w):
    if type(w) == IntType or type(w) == FloatType:
        return Vec2(v.x+w, v.y + w)
    else:
        return Vec2(v.x+w.x, v.y + w.y)

def subV2 (v,w):
    if type(w) == IntType or type(w) == FloatType:
        return Vec2(v.x-w, v.y - w)
    else:
        return Vec2(v.x-w.x, v.y - w.y)

def projectionV2(v,w):
    # The signed length of the projection of vector v on vector w.
    return dotV2(v,w)/w.length()

def squareV2(vec):
    try:
        return Vec2(vec.x**2, vec.y**2)
    except OverflowError:
        #print "OverflowError:", vec.x, vec.y
        try:
            x = vec.x**2
        except:
            x = 0.0
        try:
            y = vec.y**2
        except:
            y = 0.0
        return Vec2(x,y)

def crossV2(obj1, obj2):
    return Vec2(obj1.y*obj2.z-obj1.x*obj2.y,
    obj1.y*obj2.x-obj1.x*obj2.y)


class Vec2:
    def __init__(self,x=0.,y=0.):
        self.x = float(x)
        self.y = float(y)

    def copy(self,vec):
        self.x = vec.x
        self.y = vec.y

    def getDataPtr(self):
        return (self.x, self.y)

    def __add__(self, obj):
        if type(obj) == IntType or type(obj) == FloatType:
            return Vec2(self.x+obj, self.y + obj)
        else:
            return Vec2(self.x+obj.x, self.y + obj.y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __eq__(self, v2):
        if self.x == v2.x and self.y == v2.y:
            return True
        return False

    def __ne__(self, v2):
        if self.x != v2.x or self.y != v2.y:
            return True
        return False

    def normalize(self): # normalize to a unit vector
        self.scale(1.0/self.length())

    def truncate(self, max): # make length not exceed max
        if self.length() > max:
            self.normalize()
            self.scale(max)
        return self

    def scale(self, amount):
        self.x *= amount
        self.y *= amount

    def getSquare(self):
        return Vec2(self.x**2, self.y**2)

    def square(self):
        # square the components
        self.x **= 2
        self.y **= 2

    def getUnitNormal(self):
        return self.getScaledV2(1.0/self.length())

    def getScaledV2(self, amount):
        return Vec2u(self.x*amount, self.y*amount)

    def getNorm(self):
        # return square length: x*x + y*y
        return sumV2(squareV2(self))

    lengthSquared = getNorm

    def getPerp(self):
        return Vec2(-self.y, self.x)

    def length(self):
        # print "vec len A:", self.getNorm()
        return math.sqrt(self.getNorm())

    def __getitem__(self, index):
        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y
        raise IndexError("Vector index out of range")

    def dot(self, vec):
        # The dot product of two vectors
        #return sum( [ x*y for x,y in zip(self.data,vec.data) ] )
        return self.x*vec.x + self.y*vec.y

    def getY(self):
        return self.y

    def setY(self, val):
        self.y = val

    def set(self, x, y):
        self.x = x
        self.y = y

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

if __name__=="__main__":
    a = Vec2(1, 2)
    print "a:", a
    print "a + 5", a + 5
    print "a * 5", a * 5
    print "a - a", a -a
    b = Vec2(a.x, a.y)
    b -= 5
    print "b -= 5", b

