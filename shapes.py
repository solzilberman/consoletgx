import curses
import math
import linalg


def _line_factory(p1, p2):
    x1, x2 = round(p1.x), round(p2.x)
    y1, y2 = round(p1.y), round(p2.y)
    if x1 == x2:
        return [Point(p1.x, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
    slope = (y2 - y1) / (x2 - x1)
    y_intercept = round(y1 - slope * x1)
    fn = lambda x: round(slope * x) + y_intercept
    line = [Point(x, fn(x)) for x in range(min(x1, x2), max(x1, x2) + 1)]
    return line


def _inside_triangle(p, p1, p2, p3):
    # https://en.wikipedia.org/wiki/Barycentric_coordinate_system
    w1 = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w2 = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w3 = 1.0 - w1 - w2
    one = w1 < -0.001
    two = w2 < -0.001
    three = w3 < -0.001

    return (one == two) and (two == three)


class Rectangle:
    def __init__(self, screen, x, y, width, height):
        self.width = width
        self.height = height
        self.x = round(x)
        self.y = round(y)
        self.chars = {
            "ULC": 0x284F,
            "URC": 0x28B9,
            "BLC": 0x28C7,
            "BRC": 0x28F8,
            "U": 0x2809,
            "B": 0x28C0,
            "L": 0x2847,
            "R": 0x28B8,
            "I": 0x2800,
            "FILLED": 0x28FF,
        }

        self.noFill = False
        self.fill = 1

    def draw(self, sc):
        height = min(self.height, sc.bheight - self.y)
        width = min(self.width, sc.bwidth - self.x)
        for y in range(self.y, self.y + height):
            for x in range(self.x, self.x + width):
                if self.noFill:
                    if (
                        x == self.x
                        or x == self.x + width - 1
                        or y == self.y
                        or y == self.y + height - 1
                    ):
                        sc.BUFFER[y // 4][x // 2] |= sc.dots[y % 4][x % 2]
                else:
                    sc.BUFFER[y // 4][x // 2] |= sc.dots[y % 4][x % 2]

    def setFill(self, c):
        self.fill = 0 if c == -1 else c
        self.noFill = c == -1

    def getFill(self):
        return -1 if self.noFill else self.fill

    def translate(self, x, y):
        self.x += x
        self.y += y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, sc):
        sc.BUFFER[int(self.y // 4)][int(self.x // 2)] |= sc.dots[int(self.y) % 4][
            int(self.x) % 2
        ]


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, sc):
        minx, miny = max(0, round(min(self.p1.x, min(self.p2.x, self.p3.x)))), max(
            0, round(min(self.p1.y, min(self.p2.y, self.p3.y)))
        )
        maxx, maxy = min(
            sc.bwidth, math.ceil(max(self.p1.x, max(self.p2.x, self.p3.x)))
        ), min(sc.bheight, math.ceil(max(self.p1.y, max(self.p2.y, self.p3.y))))
        for y in range(miny, maxy):
            for x in range(minx, maxx):
                if _inside_triangle(Point(x, y), self.p1, self.p2, self.p3):
                    sc.BUFFER[y // 4][x // 2] |= sc.dots[y % 4][x % 2]

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
    def __init__(self, center, sides, radius):
        self.cx = center.x
        self.cy = center.y
        self.sides = sides
        self.radius = radius
        self.degree = float(360) / self.sides
        self.rot = float(45)

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
            tri = Triangle(p1, p2, Point(self.cx, self.cy))
            tri.draw(sc)

    def rotate(self, angle):
        self.rot += float(angle)
