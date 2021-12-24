from linalg import *

__docformat__ = "google"


class Camera:
    """
    Virtual Camera class for 3D graphics.
    Attributes:
        eye: vec3, position of the camera in world space
    """

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
        """
        Update cameras view matrix based on current camera position and target.
        """
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
        """
        Get current view matrix.
        """
        if debug:
            print("VIEW MATRIX:")
            print(f"{self.view[0].x},{self.view[0].y},{self.view[0].z}, {self.view[0].w}")
            print(f"{self.view[1].x},{self.view[1].y},{self.view[1].z}, {self.view[1].w}")
            print(f"{self.view[2].x},{self.view[2].y},{self.view[2].z}, {self.view[2].w}")
            print(f"{self.view[3].x},{self.view[3].y},{self.view[3].z}, {self.view[3].w}")
            print("=================================================================")
        return self.view

    def translate_light(self, v):
        """
        Translate the light position by vec4 v.
        """
        self.light_pos += v

    def translate_eye(self, v3):
        """
        Translate the camera position by vec3 v.
        """
        self.eye += v3
        self.look_at(self.target)

    def get_eye(self):
        """
        Returns current camera position in world space.
        """
        return self.eye

    def get_light(self):
        """
        Returns current light position in world space.
        """
        return self.light_pos
