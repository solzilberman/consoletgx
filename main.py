#!/usr/bin/python
import curses, random
import time
import shapes

# fmt: off
dots = ((0x01, 0x08),
        (0x02, 0x10),
        (0x04, 0x20),
        (0x40, 0x80))
# fmt: on


class Console:
    def __init__(self):
        self.dots = dots
        self.screen = curses.initscr()
        self.width = self.screen.getmaxyx()[1]
        self.height = self.screen.getmaxyx()[0]
        self.size = self.width * self.height
        self.char = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
        self.fill = 0
        self.BUFFER = [0] * ((self.width) * (self.height) - 1)
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
        c = self.screen.getch()
        if c == 3:
            raise KeyboardInterrupt
        self.screen.refresh()
        time.sleep(ms)
        return


offset = 0
sc = Console()
try:
    while 1:
        offset = (offset + 1) % sc.width
        sc.screen.clear()
        
        rec = shapes.Rectangle(sc, 0, offset, 5, 5)
        rec.setFill(-1)
        rec.draw(sc)

        sc.update(.1)

except KeyboardInterrupt:
    curses.endwin()
    print("exit sig recieved!")
