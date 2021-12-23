from consoletgx import *
import copy

# initialize Console object
sc = ConsoleTGX()


def checkNeighbors(x, y, curr):
    # check game of life neighbors given coords x,y
    # return number of neighbors
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x + i < 0 or x + i >= len(curr) or y + j < 0 or y + j >= len(curr[0]):
                continue
            if curr[x + i][y + j].MODE != "LINE":
                neighbors += 1
    return neighbors


# try loop will catch user kill signal ctrl+c
try:

    curr = []  # initialize current generation to dead cells
    for i in range(0, sc.width):
        tmp = []
        for j in range(0, sc.height):
            # creates new Rectangle object with upper left corner at i*4,j*4 and width 5, height 5
            r = Polygon(vec2(i * 4, j * 4), 4, 5)
            r.MODE = "LINE" if random.choice([0, 1]) == 0 else "FILL"  # sets fill to -1 or 0 randomly
            tmp.append(r)
        curr.append(tmp)

    curr[0][0].MODE = "FILL"
    # game loop will run until user kills program
    while 1:
        # clear current pixel buffer and terminal window
        sc.clear()

        next = copy.deepcopy(curr)  # initialize next generation to current generation
        # update
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                if checkNeighbors(i, j, curr) < 2 or checkNeighbors(i, j, curr) > 3:
                    next[i][j].MODE = "FILL"
                if checkNeighbors(i, j, curr) == 3:
                    next[i][j].MODE = "LINE"
        curr = copy.deepcopy(next)

        # drawing loop
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                curr[i][j].draw(sc)  # adds each cell to pixel buffer

        sc.update(0.1)  # update screen with pixel buffer and delay


except KeyboardInterrupt:
    curses.endwin()
    print("exit sig recieved!")
