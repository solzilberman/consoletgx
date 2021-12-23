from consoletgx import *

if __name__ == "__main__":
    sc = ConsoleTGX()
    camera = Camera(vec3(0, 15, 15))
    off = 0
    try:
        with open("./examples/cube.obj", "r") as f:
            data = f.read().splitlines()

        # build cube
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

            # calculate normal given 3 points in curr
            n = normalize(cross(curr[1] - curr[0], curr[2] - curr[0]))
            tri.append(Triangle3(curr[0], curr[1], curr[2], normal=n, MODE="LINE"))

        off = 15

        # animation loop
        while True:
            sc.clear()
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
