width = 10
height = 10

grid = [[0x2800 for x in range(width)] for y in range(height)]


# fmt: off
dots = ((0x01, 0x08),
        (0x02, 0x10),
        (0x04, 0x20),
        (0x40, 0x80))
# fmt: on


for y in range(0, 5):
    for x in range(0, 5):
        grid[y // 4][x // 2] |= dots[y % 4][x % 2]

print([[chr(x) for x in row] for row in grid])

for i in range(15):
    print(i % 4, i // 4)
