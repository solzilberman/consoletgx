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
            if curr[x + i][y + j].getFill() != -1:
                neighbors += 1
    return neighbors


# try loop will catch user kill signal ctrl+c
try:

    curr = []  # initialize current generation to dead cells
    for i in range(0, sc.width):
        tmp = []
        for j in range(0, sc.height):
            # creates new Rectangle object with upper left corner at i*4,j*4 and width 5, height 5
            r = shapes.Rectangle(
                sc, i * 4, j * 4, 5, 5
            )  
            r.setFill(random.choice([0,-1]))  # sets fill to -1 or 0 randomly
            tmp.append(r)
        curr.append(tmp)

    curr[0][0].setFill(1)
    # game loop will run until user kills program
    while 1:
        # clear current pixel buffer and terminal window
        sc.clear()

        next = copy.deepcopy(curr)  # initialize next generation to current generation
        # update
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                if checkNeighbors(i, j, curr) < 2 or checkNeighbors(i, j, curr) > 3:
                    next[i][j].setFill(-1)
                if checkNeighbors(i, j, curr) == 3:
                    next[i][j].setFill(0)
        curr = copy.deepcopy(next)

        # drawing loop
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                curr[i][j].draw(sc)  # adds each cell to pixel buffer

        sc.update(.1)  # update screen with pixel buffer and delay


except KeyboardInterrupt:
    curses.endwin()
    print("exit sig recieved!")
