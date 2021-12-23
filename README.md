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
