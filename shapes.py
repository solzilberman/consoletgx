import curses
import math


def _line_factory(p1, p2):
    x1, x2 = p1.x, p2.x
    y1, y2 = p1.y, p2.y
    if x1 == x2:
        return [Point(p1.x, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
    slope = (y2 - y1) / (x2 - x1)
    y_intercept = round(y1 - slope * x1)
    fn = lambda x: round(slope * x) + y_intercept
    line = [Point(x, fn(x)) for x in range(min(x1, x2), max(x1, x2) + 1)]
    return line


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
        self.x = round(x)
        self.y = round(y)

    def draw(self, sc):
        sc.BUFFER[self.y // 4][self.x // 2] |= sc.dots[self.y % 4][self.x % 2]


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, sc):
        l1 = _line_factory(self.p1, self.p2)
        l2 = _line_factory(self.p2, self.p3)
        l3 = _line_factory(self.p3, self.p1)
        for e1, e2, e3 in zip(l1, l2, l3):
            e1.draw(sc)
            e2.draw(sc)
            e3.draw(sc)

    def rotate(self, theta):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = self.p3.x, self.p3.y
        rot = lambda x, y: (
            round(x * math.cos(theta) + y * math.sin(theta)),
            round(x * math.sin(theta) - y * math.cos(theta)),
        )
        self.p1.x, self.p1.y = rot(x1, y1)
        self.p2.x, self.p2.y = rot(x2, y2)
        self.p3.x, self.p3.y = rot(x3, y3)
