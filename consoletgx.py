#!/usr/bin/python
import curses, random
import time
import random
import shapes
import math

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
        self.fill = 0
        self.BUFFER = [[0x2800 for _ in range(self.width)] for _ in range(self.height)]
        self.bg_color = 0
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, 1, 0)
        curses.init_pair(2, 2, 0)
        curses.init_pair(3, 3, 0)
        curses.init_pair(4, 4, 0)
        self.objs = []
        self.screen.clear

    def update(self, ms):
        self.screen.nodelay(1)
        for y in range(self.height - 1):
            self.screen.addstr(
                y,
                0,
                "".join(list(map(lambda x: chr(x), self.BUFFER[y]))),
                curses.color_pair(self.fill),
            )

        c = self.screen.getch()
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
    off = 0
    try:
        while True:
            off += 1
            sc.clear()
            p1 = shapes.Point(25 + off, 25)
            p2 = shapes.Point(40 + off, 25)
            p3 = shapes.Point(25 + off, 40)
            tri = shapes.Triangle(p1, p2, p3)
            tri.draw(sc)
            sc.update(0.5)
    except KeyboardInterrupt:
        curses.endwin()
        print("exit sig recieved!")
