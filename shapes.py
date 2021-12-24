import curses
import math
from linalg import *
from camera import *

__docformat__ = "google"


def euclid_distance(p1, p2):
    """
    return euclidian distance between 2 3d points
    """
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)


def area_triangle(p1, p2, p3):
    """
    Finds area of a triangle
    """
    return abs((p1.x * p2.y + p2.x * p3.y + p3.x * p1.y - p1.y * p2.x - p2.y * p3.x - p3.y * p1.x) / 2)


def lighting(p, normal, light_pos=vec4(0, 15, 0, 0)):
    """
    Calculates lighting based on vertex position, normal and light position
    """
    # https://www.scratchapixel.com/code.php?id=26&origin=/lessons/3d-basic-rendering/rasterization-practical-implementation
    light_dir = normalize(light_pos - p)
    diff = max(0, dot(normal, light_dir))
    print(p.x, p.y, p.z)
    return round((diff - 0) / (1) * (255 - 240) + 240)


def _rasterize(p, sc, cam):
    """
    Converts point from camera space to screen space
    """
    f = 100
    n = 1
    scale = math.tan(75 * 0.5 / 180 * math.pi) * n
    r = (sc.bwidth / sc.bheight) * scale
    l = -r
    t = scale
    b = -t

    # camera space -> screen space
    sx = n * p.x / -p.z
    sy = n * p.y / -p.z

    # screen space -> ndc space
    ndcx = 2 * sx / (r - l) - (r + l) / (r - l)
    ndcy = 2 * sy / (t - b) - (t + b) / (t - b)

    # ndc space -> pixel space
    half_w = sc.bwidth / 2
    half_h = sc.bheight / 2
    x_screen = max(0, min(sc.bwidth - 1, ndcx * half_w + half_w))
    y_screen = max(0, min(sc.bheight - 1, half_h - ndcy * half_h))
    z_screen = -cam.eye.z

    return vec4(x_screen, y_screen, z_screen, 1)


def _to_screen_space(p, sc):
    """
    Converts from camera space to screen space
    """
    half_w = sc.bwidth / 2
    half_h = sc.bheight / 2
    x_screen = max(0, min(sc.bwidth - 1, p.x * half_w + half_w))
    y_screen = max(0, min(sc.bheight - 1, half_h - p.y * half_h))
    return vec2(x_screen, y_screen)


def _line_factory(p1, p2):
    """
    Returns array of points on the line between [p1,p2]
    """
    x1, x2 = int(round(p1.x)), int(round(p2.x))
    y1, y2 = int(round(p1.y)), int(round(p2.y))
    xd = max(x1, x2) - min(x1, x2)
    yd = max(y1, y2) - min(y1, y2)
    r = max(xd, yd)
    dirx = 1 if x1 <= x2 else -1
    diry = 1 if y1 <= y2 else -1
    ret = []
    for i in range(r + 1):
        x = x1
        y = y1
        if yd:
            y += (float(i) * yd) / r * diry
        if xd:
            x += (float(i) * xd) / r * dirx
        ret.append(Point(round(x), round(y)))
    return ret


def _inside_triangle(p, p1, p2, p3):
    """
    Checks if a point is inside a triangle
    """
    # https://en.wikipedia.org/wiki/Barycentric_coordinate_system
    w1 = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w2 = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w3 = 1.0 - w1 - w2
    return (w1, w2, w3)


class Point:
    """
    2D Point representing pixel in screen space
    Attributes:
        x,y : coordinates of point
        (OR)
        v   : vec2, vec3, vec4 where v.x, v.y are coordinates in screen space
    """

    def __init__(self, *argv):
        if len(argv) == 2:
            self.x = argv[0]
            self.y = argv[1]
        else:
            self.x = argv[0].x
            self.y = argv[0].y

    def draw(self, sc, col=0, depth=0):
        """
        Draw point at self.x, self.y in terminal
        Parameters:
            sc               : screen object
            (optional) col   : color of point
            (optional) depth : depth of 3d point
        """
        self.x = max(0, min(self.x, sc.bwidth - 1))
        self.y = max(0, min(self.y, sc.bheight - 1))
        if depth >= sc.DEPTH_BUFFER[int(self.y // 4)][int(self.x // 2)]:
            sc.DEPTH_BUFFER[int(self.y // 4)][int(self.x // 2)] = depth
            sc.COLOR_BUFFER[int(self.y // 4)][int(self.x // 2)] = col
        sc.BUFFER[int(self.y // 4)][int(self.x // 2)] |= sc.dots[int(self.y) % 4][int(self.x) % 2]


class Triangle:
    def __init__(self, p1, p2, p3, MODE="FILL"):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.MODE = MODE

    def draw(self, sc):

        if self.MODE == "LINE":
            for p in _line_factory(self.p1, self.p2):
                p.draw(sc)
            for p in _line_factory(self.p2, self.p3):
                p.draw(sc)
            for p in _line_factory(self.p3, self.p1):
                p.draw(sc)
            return

        minx, miny = max(0, round(min(self.p1.x, min(self.p2.x, self.p3.x)))), max(
            0, round(min(self.p1.y, min(self.p2.y, self.p3.y)))
        )
        maxx, maxy = min(sc.bwidth, math.ceil(max(self.p1.x, max(self.p2.x, self.p3.x)))), min(
            sc.bheight, math.ceil(max(self.p1.y, max(self.p2.y, self.p3.y)))
        )
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                pcurr = Point(x, y)
                w1, w2, w3 = _inside_triangle(pcurr, self.p1, self.p2, self.p3)
                if self.MODE == "FILL":
                    if ((w1 < -0.001) == (w2 < -0.001)) and ((w2 < -0.001) == (w3 < -0.001)):
                        pcurr.draw(sc)

    def rotate(self, theta):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = self.p3.x, self.p3.y
        cx, cy = (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3

        rot = lambda x, y: (
            (x) * math.cos(theta) - (y) * math.sin(theta),
            (x) * math.sin(theta) + (y) * math.cos(theta),
        )

        x1 -= cx
        y1 -= cy
        x2 -= cx
        y2 -= cy
        x3 -= cx
        y3 -= cy

        nx1, ny1 = rot(x1, y1)
        nx2, ny2 = rot(x2, y2)
        nx3, ny3 = rot(x3, y3)

        self.p1.x = nx1 + cx
        self.p1.y = ny1 + cy
        self.p2.x = nx2 + cx
        self.p2.y = ny2 + cy
        self.p3.x = nx3 + cx
        self.p3.y = ny3 + cy


class Polygon:
    def __init__(self, center, sides, radius, MODE="FILL"):
        self.cx = center.x
        self.cy = center.y
        self.sides = sides
        self.radius = radius
        self.degree = float(360) / self.sides
        self.rot = float(45)
        self.MODE = MODE

    def draw(self, sc):
        for n in range(self.sides):
            a = (n * self.degree + self.rot) % 360
            b = ((n + 1) * self.degree + self.rot) % 360
            p1 = Point(
                self.cx + math.cos(math.radians(a)) * (self.radius + 1) / 2,
                self.cy + math.sin(math.radians(a)) * (self.radius + 1) / 2,
            )
            p2 = Point(
                self.cx + math.cos(math.radians(b)) * (self.radius + 1) / 2,
                self.cy + math.sin(math.radians(b)) * (self.radius + 1) / 2,
            )
            tri = Triangle(p1, p2, Point(self.cx, self.cy), self.MODE)
            tri.draw(sc)

    def rotate(self, angle):
        self.rot += float(angle)


class Point3:
    def __init__(self, v):
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def draw(self, sc, col=0):
        x_screen = self.x
        y_screen = self.y
        sc.BUFFER[int(y_screen // 4)][int(x_screen // 2)] |= sc.dots[int(y_screen) % 4][int(x_screen) % 2]
        sc.COLOR_BUFFER[int(y_screen // 4)][int(x_screen // 2)] = col


class Triangle3:
    """
    3D Triangle class
    Attributes:
        p1, p2, p3: vec4 vertices of triangle
        normal: vec4 normal of triangle
        MODE: drawing mode, "FILL" or "LINE"
    """

    def __init__(self, p1, p2, p3, normal=vec4(0, 0, 0, 0), MODE="FILL"):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.MODE = MODE
        self.normal = normal

    def draw(self, sc, c):
        """
        Draws the triangle on the screen
        Parameters:
            sc : screen object
            c  : camera object
        """
        # world space -> camera space
        v1 = multiply(self.p1, transpose(c.get_view()))
        v2 = multiply(self.p2, transpose(c.get_view()))
        v3 = multiply(self.p3, transpose(c.get_view()))
        # camera space -> pixel space
        vp1 = _rasterize(v1, sc, c)
        vp2 = _rasterize(v2, sc, c)
        vp3 = _rasterize(v3, sc, c)
        vp1.z = 1 / vp1.z
        vp2.z = 1 / vp2.z
        vp3.z = 1 / vp3.z

        ps1 = vp1
        ps2 = vp2
        ps3 = vp3
        area = area_triangle(ps1, ps2, ps3)
        # shade
        light_dir = normalize(c.get_light() - self.p1)
        diff = max(0, dot(self.normal, light_dir))
        diff = round((diff - 0) / (1) * (255 - 240) + 240)

        if self.MODE == "LINE":
            for p in _line_factory(ps1, ps2):
                p.draw(sc, diff)
            for p in _line_factory(ps2, ps3):
                p.draw(sc, diff)
            for p in _line_factory(ps3, ps1):
                p.draw(sc, diff)
            return

        minx, miny = max(0, round(min(ps1.x, min(ps2.x, ps3.x)))), max(0, round(min(ps1.y, min(ps2.y, ps3.y))))
        maxx, maxy = min(sc.bwidth, math.ceil(max(ps1.x, max(ps2.x, ps3.x)))), min(
            sc.bheight, math.ceil(max(ps1.y, max(ps2.y, ps3.y)))
        )
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                pcurr = Point(x, y)
                w1, w2, w3 = _inside_triangle(pcurr, ps1, ps2, ps3)
                if self.MODE == "FILL":
                    if ((w1 < -0.001) == (w2 < -0.001)) and ((w2 < -0.001) == (w3 < -0.001)):
                        nw1 = w1 / area
                        nw2 = w2 / area
                        nw3 = w3 / area
                        z = -1 / (nw1 * ps1.z + nw2 * ps2.z + nw3 * ps3.z)
                        pcurr.draw(sc, diff, z)

    def rotate(self, theta, axis):
        """
        Rotates self.p1, self.p2,self.p3 around axis by theta
        """
        axis = axis.lower()
        if axis == "y":
            self.p1 = rotateY(self.p1, theta)
            self.p2 = rotateY(self.p2, theta)
            self.p3 = rotateY(self.p3, theta)
            self.normal = rotateY(self.normal, theta)
        elif axis == "x":
            self.p1 = rotateX(self.p1, theta)
            self.p2 = rotateX(self.p2, theta)
            self.p3 = rotateX(self.p3, theta)
        elif axis == "z":
            self.p1 = rotateZ(self.p1, theta)
            self.p2 = rotateZ(self.p2, theta)
            self.p3 = rotateZ(self.p3, theta)

    def scale(self, factor):
        self.m = [
            vec4(factor, 0, 0, 0),
            vec4(0, factor, 0, 0),
            vec4(0, 0, factor, 0),
            vec4(0, 0, 0, 1),
        ]
        self.p1 = multiply(self.p1, self.m)
        self.p2 = multiply(self.p2, self.m)
        self.p3 = multiply(self.p3, self.m)


class Sphere:
    """
    3D Sphere Object
    Attributes:
        center : center of the sphere
        radius : radius of the sphere
        MODE   : mode of drawing, "FILL" or "LINE
    """

    def __init__(self, c, radius, MODE="FILL"):
        self.cx = c.x
        self.cy = c.y
        self.cz = c.z
        self.cw = c.w
        self.radius = radius
        self.MODE = MODE

    def draw(self, sc, c):
        """
        Draws the sphere on the screen
        Parameters:
            sc : screen object
            c  : camera object
        """
        # world space -> camera space
        # http://www.songho.ca/opengl/gl_sphere.html
        sector_count = 50
        sector_step = 2 * math.pi / sector_count
        stack_step = math.pi / sector_count
        sector_angle = 0
        stack_angle = 0
        length_inv = 1 / self.radius
        for i in range(sector_count):
            stack_angle = math.pi / 2 - i * stack_step
            xy = self.radius * math.cos(stack_angle)
            z = self.radius * math.sin(stack_angle)
            for j in range(sector_count):
                sector_angle = j * sector_step
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                p = vec4(self.cx + x, self.cy + y, self.cz + z, 1)
                # camera space -> pixel space
                p = multiply(p, transpose(c.get_view()))
                p = _rasterize(p, sc, c)
                p.z = 1 / p.z
                pcurr = Point(p.x, p.y)

                nx = x * length_inv
                ny = y * length_inv
                nz = z * length_inv
                col = lighting(p, vec4(nx, ny, nz, 0), c.light_pos)

                pcurr.draw(sc, col)
