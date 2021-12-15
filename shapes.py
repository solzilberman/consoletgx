import curses


class Rectangle:
    def __init__(self, screen, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.chars = {
            "ULC": 0x284F,
            "URC": 0x28B9,
            "BLC": 0x28C7,
            "BRC": 0x28F8,
            "U":   0x2809,
            "B":   0x28C0,
            "L":   0x2847,
            "R":   0x28B8,
            "I":   0x2800,
            "FILLED": 0x28FF,
        }

        self.noFill = False
        self.fill = 1

    def typePix(self, x, y,w,h):
        # determine if pixel is corner
        if x == self.x and y == self.y:
            return "ULC"
        elif x == self.x and y == self.y + h - 1:
            return "BLC"
        elif x == self.x + w - 1 and y == self.y:
            return "URC"
        elif x == self.x + w - 1 and y == self.y + h - 1:
            return "BRC"
        # determine if pixel is side
        elif (x == self.x and y > self.y and y < self.y + h - 1):
            return "L"
        elif (x == self.x + w - 1 and y > self.y and y < self.y + h - 1):
            return "R"
        # determine if pixel is up/bottom
        elif (y == self.y and x > self.x and x < self.x + w - 1): 
            return "U"
        elif (y == self.y + h - 1 and x > self.x and x < self.x + w - 1):
            return "B"
        return "I"

    def draw(self, sc):
        
        grid=[[0x2800 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(0,self.height):
            for x in range(0,self.width):
                if self.noFill:
                    if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                         grid[y//4][x//2] |= sc.dots[y%4][x%2]
                else:
                    grid[y//4][x//2] |= sc.dots[y%4][x%2]
            sc.screen.addstr(self.y+(y//4),self.x,  ''.join(list(map(lambda x: chr(x), grid[y//4]))), curses.color_pair(self.fill))


    def setFill(self, c):
        self.fill = 0 if c == -1 else c
        self.noFill = c == -1

    def translate(self, x, y):
        self.x += x
        self.y += y
