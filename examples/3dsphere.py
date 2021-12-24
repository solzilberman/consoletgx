from consoletgx import *

if __name__ == "__main__":
    sc = ConsoleTGX()
    camera = Camera(vec3(0, 15, 15))
    off = 0
    sph = Sphere(vec4(0, 0, 0, 0), 10, MODE="LINE")
    try:

        # animation loop
        while True:
            sc.clear()
            sph.draw(sc, camera)
            camera.move_light(vec4(5, 0, 0, 0))
            sc.update(0.1)

            c = sc.screen.getch()
            if c == 3:
                raise KeyboardInterrupt
            elif c == 259:
                camera.get_view(debug=True)
    except KeyboardInterrupt:
        curses.endwin()
        print("exit sig recieved!")
