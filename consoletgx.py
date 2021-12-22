#!/usr/bin/python
import curses, random
import time
import random
from shapes import *
import math
from camera import *
from linalg import *
from sshkeyboard import listen_keyboard


PI = math.pi
# fmt: off
dots = ((0x01, 0x08),
        (0x02, 0x10),
        (0x04, 0x20),
        (0x40, 0x80))
# fmt: on


class ConsoleTGX:
    def __init__(self):
        self.dots = dots
        self.screen = curses.initscr()
        self.width = self.screen.getmaxyx()[1]
        self.height = self.screen.getmaxyx()[0]
        self.bwidth = self.width * 2
        self.bheight = self.height * 4
        self.size = self.width * self.height
        self.bsize = self.bwidth * self.bheight
        self.fill = 3
        self.BUFFER = [[0x2800 for _ in range(self.width)] for _ in range(self.height)]
        self.bg_color = 0
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self.screen.keypad(1)
        # curses.init_pair(1, 1, 0)
        # curses.init_pair(2, 2, 0)
        # curses.init_pair(3, 3, 0)
        # curses.init_pair(4, 4, 0)
        self.objs = []
        self.screen.clear

    def update(self, ms):
        self.screen.nodelay(1)
        for y in range(self.height - 1):
            self.screen.addstr(
                y,
                0,
                "".join(list(map(lambda x: chr(x), self.BUFFER[y]))),
                curses.color_pair(4),
            )

        c = sc.screen.getch()
        if c == 3:
            raise KeyboardInterrupt

        self.screen.refresh()
        time.sleep(ms)
        return

    def clear(self):
        self.BUFFER = [[0x2800 for _ in range(self.width)] for _ in range(self.height)]
        self.screen.erase()


if __name__ == "__main__":
    sc = ConsoleTGX()
    camera = Camera(vec3(0, 15, 15))
    off = 0
    camera.get_view(debug=True)
    try:
        with open("./tests/cube.obj", "r") as f:
            data = f.read().splitlines()

        tri = []
        for i in range(0, len(data) - 2, 3):
            curr = []
            for j in range(3):
                av = list(
                    filter(
                        lambda s: type(s) == float,
                        map(lambda s: float(s) if len(s) > 0 else int(0), data[i + j].split(",")),
                    )
                )
                curr.append(vec4(av[0], av[1], av[2], 1))

            tri.append(Triangle3(curr[0], curr[1], curr[2], MODE="LINE"))

        # poly = Polygon(Point(25, 25), 5, 15, "LINE")
        off = 15
        for t in tri:
            t.rotate(off, "y")
        while True:
            sc.clear()
            # pp.rotate(PI / 8)
            for t in tri:
                t.rotate(off, "y")
                t.draw(sc, camera)
            sc.update(0.25)
            c = sc.screen.getch()

            if c == 3:
                raise KeyboardInterrupt
            elif c == 259:
                camera.translate(vec3(0, 0, 5))
                # camera.get_view(debug=True)
    except KeyboardInterrupt:
        curses.endwin()
        print("exit sig recieved!")
