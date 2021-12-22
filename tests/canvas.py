import curses

screen = curses.initscr()
width = screen.getmaxyx()[1]
height = screen.getmaxyx()[0]
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, 1, 0)
curses.init_pair(2, 2, 0)
curses.init_pair(3, 3, 0)
curses.init_pair(4, 4, 0)
try:
    while 1:
        screen.addnstr(0, 226, "hello", width - 226, curses.color_pair(1))
        c = screen.getch()
        if c == 3:
            raise KeyboardInterrupt
        screen.refresh()
except KeyboardInterrupt:
    curses.endwin()
    print("exit sig recieved!")

# width = 10
# height = 10

# grid = [[0x2800 for x in range(width)] for y in range(height)]


# # fmt: off
# dots = ((0x01, 0x08),
#         (0x02, 0x10),
#         (0x04, 0x20),
#         (0x40, 0x80))
# # fmt: on


# for y in range(0, 5):
#     for x in range(0, 5):
#         grid[y // 4][x // 2] |= dots[y % 4][x % 2]

# print([[chr(x) for x in row] for row in grid])

# for i in range(15):
#     print(i % 4, i // 4)
