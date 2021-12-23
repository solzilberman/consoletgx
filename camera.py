from linalg import *


class Camera:
    def __init__(self, eye):
        self.eye = eye
        self.up = vec3(0, 1, 0)
        self.right = vec3(1, 0, 0)
        self.forward = vec3(0, -self.eye.y, -self.eye.z)
        self.view = [[0 for i in range(4)] for j in range(4)]
        self.target = vec3(0, 0, 0)
        self.light_pos = vec4(0, 15, -15, 0)
        self.look_at(self.target)

    def look_at(self, target):
        self.target = target
        self.forward = normalize(self.eye - self.target)
        self.up = cross(self.forward, self.right)
        self.right = normalize(cross(self.up, self.forward))

        self.view = [
            vec4(self.right.x, self.up.x, -self.forward.x, 0),
            vec4(self.right.y, self.up.y, -self.forward.y, 0),
            vec4(self.right.z, self.up.z, -self.forward.z, 0),
            vec4(-dot(self.right, self.eye), -dot(self.up, self.eye), -dot(self.forward, self.eye), 1.0),
        ]

    def get_view(self, debug=False):
        if debug:
            print("VIEW MATRIX:")
            print(f"{self.view[0].x},{self.view[0].y},{self.view[0].z}, {self.view[0].w}")
            print(f"{self.view[1].x},{self.view[1].y},{self.view[1].z}, {self.view[1].w}")
            print(f"{self.view[2].x},{self.view[2].y},{self.view[2].z}, {self.view[2].w}")
            print(f"{self.view[3].x},{self.view[3].y},{self.view[3].z}, {self.view[3].w}")
            print("=================================================================")
        return self.view

    def move_light(self, v):
        self.light_pos += v

    def translate(self, v4):
        self.eye += v4
        self.look_at(self.target)
