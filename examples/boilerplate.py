from consoletgx import *

if __name__ == "__main__":
    sc = ConsoleTGX()  # init terminal screen
    camera = Camera(vec3(0, 15, 15))  # init camera at point (0,15,15)
    sph = Sphere(0, 0, 0, 10, MODE="LINE")  # init sphere at point (0,0,0) with radius 10

    try:  # try-except to exit on ctrl-c
        # animation loop
        while True:
            sc.clear()  # clear the screen
            sph.draw(sc, camera)  # add sphere vertices to framebuffer
            sc.update(0.1)  # update screen with new framebuffer

            c = sc.screen.getch()  # check for ctrl-c
            if c == 3:
                raise KeyboardInterrupt

    except KeyboardInterrupt:
        sc.exit()  # exit on ctrl-c
