from consoletgx import *

if __name__ == "__main__":
    sc = ConsoleTGX()
    camera = Camera(vec3(0, 15, 15))
    camera.light_pos = vec4(-5, 15, 0, 0)
    objl = ObjLoader()
    off = 0
    try:
        tri = objl.read("./examples/torus.obj")
        for t in tri:
            t.rotate(15, "y")
            t.scale(2.5)
        # animation loop
        while True:
            sc.clear()
            for t in tri:
                t.rotate(15, "x")
                t.draw(sc, camera)
            sc.update(0.25)
            c = sc.screen.getch()

            if c == 3:
                raise KeyboardInterrupt
            elif c == 259:
                pass
    except KeyboardInterrupt:
        sc.exit()
