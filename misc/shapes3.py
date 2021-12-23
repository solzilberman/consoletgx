import curses
import math
import linalg


def _to_screen_space(p, sc):
    return (max(0, min(p.x, sc.bwidth - 1)), max(0, min(p.y, sc.bheight - 1)))


def _line_factory(p1, p2):
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
    # https://en.wikipedia.org/wiki/Barycentric_coordinate_system
    w1 = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w2 = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / (
        (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
    )
    w3 = 1.0 - w1 - w2
    return (w1, w2, w3)


# class Polygon:
#     def __init__(self, center, sides, radius, MODE="FILL"):
#         self.cx = center.x
#         self.cy = center.y
#         self.sides = sides
#         self.radius = radius
#         self.degree = float(360) / self.sides
#         self.rot = float(45)
#         self.MODE = MODE

#     def draw(self, sc):
#         for n in range(self.sides):
#             a = (n * self.degree + self.rot) % 360
#             b = ((n + 1) * self.degree + self.rot) % 360
#             p1 = Point(
#                 self.cx + math.cos(math.radians(a)) * (self.radius + 1) / 2,
#                 self.cy + math.sin(math.radians(a)) * (self.radius + 1) / 2,
#             )
#             p2 = Point(
#                 self.cx + math.cos(math.radians(b)) * (self.radius + 1) / 2,
#                 self.cy + math.sin(math.radians(b)) * (self.radius + 1) / 2,
#             )
#             tri = Triangle(p1, p2, Point(self.cx, self.cy), self.MODE)
#             tri.draw(sc)

#     def rotate(self, angle):
#         self.rot += float(angle)
