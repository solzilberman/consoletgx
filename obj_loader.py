from shapes import *
from linalg import *


class ObjLoader:
    def __init__(self):
        pass

    def read(self, filename, MODE="FILL"):
        with open(filename, "r") as f:
            data = f.read().splitlines()

        vertex = []
        ind = []

        data = list(filter(lambda s: len(s) > 0, data))

        for line in data:
            if line[0] == "v":
                vertex.append(list(map(lambda x: float(x), line[2:].split(" "))))
            elif line[0] == "f":
                ind.append(list(map(lambda x: int(x) - 1, line[2:].split(" "))))

        triangles = []
        for tri in ind:
            curr0 = vec4(vertex[tri[0]][0], vertex[tri[0]][1], vertex[tri[0]][2], 1)
            curr1 = vec4(vertex[tri[1]][0], vertex[tri[1]][1], vertex[tri[1]][2], 1)
            curr2 = vec4(vertex[tri[2]][0], vertex[tri[2]][1], vertex[tri[2]][2], 1)
            curr = [curr0, curr1, curr2]
            n = normalize(cross(curr[1] - curr[0], curr[2] - curr[0]))
            triangles.append(Triangle3(curr[0], curr[1], curr[2], normal=n, MODE=MODE))

        return triangles


if __name__ == "__main__":
    o = ObjLoader()
    t = o.read("./examples/torus.obj")
    print(t[0])
