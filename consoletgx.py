#!/usr/bin/python
import curses
import time
import random
import math
from shapes import *
from camera import *
from linalg import *
from obj_loader import *

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
        self.COLOR_BUFFER = [[240 for _ in range(self.width)] for _ in range(self.height)]
        self.DEPTH_BUFFER = [[-100 for _ in range(self.width)] for _ in range(self.height)]
        self.bg_color = 0
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self.screen.keypad(1)
        for i in range(1, 256):
            curses.init_pair(i, i, 0)

        self.objs = []
        self.screen.clear

    def update(self, ms):
        self.screen.nodelay(1)
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                self.screen.addstr(
                    y,
                    x,
                    chr(self.BUFFER[y][x]),
                    curses.color_pair(self.COLOR_BUFFER[y][x]),
                )

        c = self.screen.getch()
        if c == 3:
            raise KeyboardInterrupt

        self.screen.refresh()
        time.sleep(ms)
        return

    def clear(self):
        self.BUFFER = [[0x2800 for _ in range(self.width)] for _ in range(self.height)]
        self.COLOR_BUFFER = [[240 for _ in range(self.width)] for _ in range(self.height)]
        self.DEPTH_BUFFER = [[-100 for _ in range(self.width)] for _ in range(self.height)]
        self.screen.erase()

    def exit(self):
        curses.endwin()
        print("exit sig recieved!")
