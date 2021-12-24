import copy
import math


class ShapeError(Exception):
    def __init__(self, a, b, f):
        """
        Thrown on shape mismatch during operation
        """
        self.a = a
        self.b = b

    def __str__(self):
        return f"ShapeError: {self.a.dim} != {self.b.dim}"


class vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        returns self.m + other.m
        """
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        returns self.m - other.m
        """
        return vec2(self.x - other.x, self.y - other.y)


class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.dim = 3
        self.xy = vec2(self.x, self.y)

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
        self.xyz = vec3(self.x, self.y, self.z)
        self.xy = vec2(self.x, self.y)

    def __add__(self, other):
        """
        return self.m + other.m
        """
        return vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        """
        return self.m - other.m
        """
        return vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)


def dot(v1, v2):
    if v1.dim != v2.dim:
        raise ShapeError(v1, v2, "dot")
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
    if type(v1) != type(v2):
        raise ShapeError(v1, v2, "cross")

    a = [v1.x, v1.y, v1.z]
    b = [v2.x, v2.y, v2.z]
    c = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]

    return vec3(c[0], c[1], c[2]) if v1.dim == 3 else vec4(c[0], c[1], c[2], 0)


def normalize(v):
    if type(v) == vec3:
        raw = copy.deepcopy(v)
        raw = [raw.x, raw.y, raw.z]
        lenv = math.sqrt(raw[0] ** 2 + raw[1] ** 2 + raw[2] ** 2)
        if lenv == 0:
            return vec3(0, 0, 0)
        return vec3(raw[0] / lenv, raw[1] / lenv, raw[2] / lenv)
    elif type(v) == vec4:
        raw = copy.deepcopy(v)
        raw = [raw.x, raw.y, raw.z, raw.w]
        lenv = math.sqrt(raw[0] ** 2 + raw[1] ** 2 + raw[2] ** 2 + raw[3] ** 2)
        if lenv == 0:
            return vec4(0, 0, 0, 0)
        return vec4(raw[0] / lenv, raw[1] / lenv, raw[2] / lenv, raw[3] / lenv)


def rotateX(v, angle):
    """Rotates the point around the X axis by the given angle in degrees."""
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y = v.y * cosa - v.z * sina
    z = v.y * sina + v.z * cosa
    return vec4(v.x, y, z, v.w)


def rotateY(v, angle):
    """Rotates the point around the Y axis by the given angle in degrees."""
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x = v.x * cosa - v.y * sina
    y = v.x * sina + v.y * cosa
    return vec4(x, y, v.z, v.w)


def rotateZ(v, angle):
    """Rotates the point around the Z axis by the given angle in degrees."""
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    z = v.z * cosa - v.x * sina
    x = v.z * sina + v.x * cosa
    return vec4(x, v.y, z, v.w)
