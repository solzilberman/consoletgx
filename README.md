# ConsoleTGX
#### 3D Graphics Engine in your terminal.

Installation:

    git clone https://github.com/solzilberman/consoletgx

Run Examples:

    mv ./examples/3dsphere.py .
    python 3dsphere.py

Basic Usage
```
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
        curses.endwin()
        print("exit sig recieved!")

```

Examples:

Spinning Cube

![Spinning Cube](https://i.imgur.com/BIxVB1f.gif)

Sphere + Basic Lighting Model

![Sphere with lighting](https://i.imgur.com/zA7iDcJ.gif)


**Important Notice** </br>
This has only been tested on windows 10 machine running in windows terminal.</br>
</br>
**Dependencies:**</br>
[python curses](https://docs.python.org/3/howto/curses.html)</br>
</br>
**REFERENCES**</br>
[Braille Patterns](https://en.wikipedia.org/wiki/Braille_Patterns)</br>
[Perspective Projection](https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/projection-matrices-what-you-need-to-know-first)</br>
[Rasterization](https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation)</br>
[OpenGL Camera](http://www.songho.ca/opengl/gl_camera.html)</br>
[Similair Project: Drawville 2d Terminal Engine](https://github.com/asciimoo/drawille)</br>
