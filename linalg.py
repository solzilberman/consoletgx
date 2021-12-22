import copy
import math

"""
Custom Exception Classes to assist in debugging and error handling
"""


class ShapeError(Exception):
    def __init__(self, a, b, mult=False):
        """
        Thrown on shape mismatch during operation
        """
        self.a = a
        self.b = b
        self.mult = mult

    def __str__(self):
        if not self.mult:
            return f"Matrix must be of same dimension but got {self.a.shape[0]} x {self.a.shape[1]} and {self.b.shape[0]} x {self.b.shape[1]} instead"
        else:
            f"ShapeError: A.shape[1] must equal B.shape[0] but got A.shape[1] = {self.a.shape[1]} and B.shape[0] = {self.b.shape[0]} instead"


class TypeOperandError(Exception):
    """
    Thrown when type mismatch between operands
    other = type(Incorrect Var)
    """

    def __init__(self, other, op):
        self.other = other
        self.op = op

    def __str__(self):
        return f'TypeError: unsupported operand type(s) for "{self.op}": "Matrix" and "{self.other}"'


class ArgError(Exception):
    """
    Thrown when arguments length is not valid
    """

    def __init__(self, args):
        self.args = args

    def __str__(self):
        return f"Expected 1 or 2 arguments but got {len(self.args)} instead"


class RectError(Exception):
    """
    Thrown when input data is not rectangular
    """

    def __str__(self):
        return f"Matrix must be rectangular"


class TypeArgError(Exception):
    """
    Thrown when constructor faces type mismatch from input data
    val = len(args)
    """

    def __init__(self, args, val):
        self.args = args
        self.val = val

    def __str__(self):
        if self.val == 1:
            return f"Arguments must be of type <int> or <list> but got <{type(self.args[0]).__name__}>"
        else:
            return f"Arguments must be of type <int, int> but got <{type(self.args[0]).__name__}, {type(self.args[1]).__name__}>"


class DetException(Exception):
    def __str__(self):
        return "Determinant Error: Matrix is not square"


class Matrix:
    def __init__(self, *args):
        self.m = None
        self.shape = [None, None]
        """
        Constructor
        ===========
        args = {
            int n : n x n matrix created or
            int m,n: m x n matrix created or
            list mat: matrix set to mat 
        }
        """
        if 2 < len(args) or len(args) < 1:
            raise ArgError(len(args))
        if len(args) == 1:
            if type(args[0]).__name__ == "int":
                # self.m := nxn matrix where n = args[0]
                self.m = [[0] * args[0] for i in range(args[0])]
                self.shape = [args[0], args[0]]
            elif type(args[0]).__name__ == "list":
                if type(args[0][0]).__name__ == "int":
                    # self.m := 1xn matrix where n = len(args[0])
                    self.m = [args[0]]
                    self.shape = [1, len(args[0])]
                elif type(args[0][0]).__name__ == "list":
                    if len({len(row) for row in args[0]}) > 1:
                        raise RectError()
                    else:
                        # self.m := m x n matrix where m,n = len(args[0]),len(args[0][0])
                        self.m = args[0]
                        self.shape = [len(args[0]), len(args[0][0])]
            else:
                raise TypeArgError(args, 1)
        elif len(args) == 2:
            # m x n matrix
            if type(args[0]).__name__ == "int" and type(args[0]).__name__ == "int":
                self.m = [[0] * args[1] for i in range(args[0])]
                self.shape = [args[0], args[1]]
            else:
                raise TypeArgError(args, 2)

    def __str__(self):
        """
        Pretty prints matrix
        """
        s = "[\n"
        for i in range(self.shape[0]):
            s += "    ["
            for j in range(self.shape[1]):
                if j < self.shape[1] - 1:
                    s += f"{self.m[i][j]}, "
                else:
                    s += f"{self.m[i][j]}"
            if i < self.shape[0] - 1:
                s += "],\n"
            else:
                s += "]"
        s += "\n]\n"
        return s

    def __add__(self, other):
        """
        returns self.m + other.m
        """
        if type(other).__name__ == "Matrix":
            if self.shape == other.shape:
                return Matrix(
                    [[self.m[i][j] + other.m[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
                )
            else:
                raise ShapeError(self, other)
        else:
            raise TypeOperandError(type(other).__name__, "+")

    def __sub__(self, other):
        """
        return self.m - other.m
        """
        if type(other).__name__ == "Matrix":
            if self.shape == other.shape:
                return Matrix(
                    [[self.m[i][j] - other.m[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]
                )
            else:
                raise ShapeError(self, other)
        else:
            raise TypeOperandError(type(other).__name__, "-")

    def __mul__(self, other):
        """
        returns self.m * other.m
        """
        if type(other).__name__ == "Matrix":
            if self.shape[1] == other.shape[0]:
                ret = [[0] * self.shape[0] for i in range(other.shape[1])]
                for i in range(self.shape[0]):
                    for j in range(other.shape[1]):
                        for k in range(self.shape[1]):
                            ret[i][j] += self.m[i][k] * other.m[k][j]
                return Matrix(ret)

            else:
                raise ShapeError(self, other, True)
        else:
            raise TypeOperandError(type(other).__name__, "*")

    @property
    def T(self):
        """
        Returns Transpose of itself
        """
        r = [[0] * self.shape[0] for i in range(self.shape[1])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                r[j][i] = self.m[i][j]
        return Matrix(r)

    def is_square(self):
        """
        Returns true if self.m is square matrix
        """
        return self.shape[0] == self.shape[1]

    def determinant(self, A):
        """
        Fast determinant calc for matrix A
        """
        n = len(A)
        ac = [row[:] for row in A]

        for d in range(n):
            if ac[d][d] == 0:
                ac[d][d] = 1.0e-18
            for i in range(d + 1, n):
                scl = ac[i][d] / ac[d][d]
                for j in range(n):
                    ac[i][j] = ac[i][j] - scl * ac[d][j]
        p = 1.0
        for i in range(n):
            p *= ac[i][i]
        return 0.0 if round(p, 10) == -0.0 or 0.0 else round(p, 10)

    @property
    def det(self):
        """
        Determinant wrapper for error checking and passing value of self.m
        """
        if self.is_square():
            return self.determinant(self.m)
        else:
            raise DetException()


class IdentityMatrix(Matrix):
    def __init__(self, n):
        id = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        super().__init__(id)


class ZerosMatrix(Matrix):
    def __init__(self, m, n):
        id = [[0 for j in range(n)] for i in range(m)]
        super().__init__(id)


class OnesMatrix(Matrix):
    def __init__(self, m, n):
        id = [[1 for j in range(n)] for i in range(m)]
        super().__init__(id)


class vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.dim = 3

    def __add__(self, other):
        """
        returns self.m + other.m
        """
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """
        return self.m - other.m
        """
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)


class vec4:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.dim = 4

    def __add__(self, other):
        """
        return self.m + other.m
        """
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        """
        return self.m - other.m
        """
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)


def dot(v1, v2):
    if v1.dim == 4:
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w
    elif v1.dim == 3:
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def transpose(m):
    ret = [
        vec4(m[0].x, m[1].x, m[2].x, m[3].x),
        vec4(m[0].y, m[1].y, m[2].y, m[3].y),
        vec4(m[0].z, m[1].z, m[2].z, m[3].z),
        vec4(m[0].w, m[1].w, m[2].w, m[3].w),
    ]
    return ret


def multiply(v, G):
    result = []
    for i in range(len(G)):
        result.append(dot(v, G[i]))
    return vec4(result[0], result[1], result[2], result[3])


def cross(v1, v2):
    a = [v1.x, v1.y, v1.z]
    b = [v2.x, v2.y, v2.z]
    c = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]

    return vec3(c[0], c[1], c[2])


def normalize(v):
    raw = copy.deepcopy(v)
    raw = [raw.x, raw.y, raw.z]
    lenv = math.sqrt(raw[0] ** 2 + raw[1] ** 2 + raw[2] ** 2)
    if lenv == 0:
        return vec3(0, 0, 0)
    return vec3(raw[0] / lenv, raw[1] / lenv, raw[2] / lenv)


def rotateY(v, angle):
    """Rotates the point around the Y axis by the given angle in degrees."""
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    z = v.z * cosa - v.x * sina
    x = v.z * sina + v.x * cosa
    return vec4(x, v.y, z, v.w)
